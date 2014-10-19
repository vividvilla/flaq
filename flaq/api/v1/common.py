from functools import wraps
import json

from flask import request, url_for
from flask.ext.restful import abort, reqparse, \
                    fields, marshal_with, marshal

from flaq import app
from flaq.models.user import User
from flaq.utils import get_sha256_hash, get_utc_timestamp

class Parsers:
    client_key_parser = reqparse.RequestParser()
    client_key_parser.add_argument(
        'Public-Key', type=str,
        location='headers',
        required=True)
    client_key_parser.add_argument(
        'Signature', type=str,
        location='headers',
        required=True)
    client_key_parser.add_argument(
        'Expiry-Time', type=str,
        location='headers',
        required=True)

    password_parser = reqparse.RequestParser()
    password_parser.add_argument(
        'password', type=str, required=True, location='form')

class OutputFields:
    role_fields = {
        'name': fields.String(attribute='title'),
        'id': fields.Integer(attribute='id'),
        'uri': fields.Url('user_endpoint', absolute=True)
    }

    user_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String,
        'full_name': fields.String(attribute='real_name'),
        'website': fields.String(default=None),
        'bio': fields.String(default=None),
        'created_date': fields.DateTime,
        'modified_date': fields.DateTime,
        'uri': fields.Url('user_endpoint', absolute=True),
        'role': fields.Nested(role_fields),
    }

def user_existance_check(username):
    try:
        user = User.get(username)
        return user
    except ValueError:
        abort(404, error="Username {} doesn't exist".format(username))

def get_private_key(public_key):
    client_secret = app.config["CLIENT_SECRET"]
    if public_key and public_key in client_secret:
        return client_secret[public_key]
    abort(401, error="Unknown Public-Key in HTTP header")

def check_signature(private_key, data):
    signature = data["Signature"]
    expiry = data["Expiry-Time"]

    check_request_expiry(expiry)

    new_signature = get_sha256_hash(expiry + private_key)
    if not (signature == new_signature):
        abort(401, error="Invalid signature")

def check_request_expiry(time_stamp):
    if(float(time_stamp) < get_utc_timestamp()):
        abort(401, error = "Expired request")

    if(float(time_stamp) > get_utc_timestamp(15)):
        abort(400, error = "Expiry cannot be more than 15 minutes")

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
        private_key = get_private_key(req_args["Public-Key"])
        check_signature(private_key, req_args)
        return func(*args, **kwargs)
    return wrapper