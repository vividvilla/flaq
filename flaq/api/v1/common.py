from functools import wraps

from flask import request
from flask.ext.restful import abort, reqparse

from flaq import app
from flaq.models.user import User


class Parsers:
    client_key_parser = reqparse.RequestParser()
    client_key_parser.add_argument(
        'Public-Key', type=str,
        location='headers',
        required=True)
    client_key_parser.add_argument(
        'Signature', type=str,
        location='header',
        required=True)

    password_parser = client_key_parser
    password_parser.add_argument(
        'password', type=str, required=True, location='form')

def user_existance_check(username):
    try:
        user = User.get(username)
        return user
    except ValueError:
        abort(404, message="Username {} doesn't exist".format(username))

def get_private_key(public_key):
    client_secret = app.config["CLIENT_SECRET"]
    if public_key and public_key in client_secret:
        return client_secret[public_key]
    abort(401, message="Unknown Public-Key in HTTP header")

def check_signature(private_key, headers, data):
    pass

#Decorators
def verify_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req_args = Parsers.client_key_parser.parse_args()
        private_key = get_private_key(req_args["Public-Key"])
        return func(*args, **kwargs)
    return wrapper

def verify_signature(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req_args = Parsers.client_key_parser.parse_args()
        req_headers = request.headers
        private_key = get_private_key(req_args["Public-Key"])
        check_signature(private_key, req_args, req_headers)
        return func(*args, **kwargs)
    return wrapper