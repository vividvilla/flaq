from functools import wraps
import json

from flask import request, url_for
from flask.ext.restful import abort, reqparse, \
                    fields, marshal_with, marshal

from flaq import app
from flaq.models.user import User
from flaq.utils import get_utc_timestamp, verify_bcrypt_hash

#Custom parsers
class Parsers:
    '''Parser for all api endpoints'''
    #Client authentication parsers
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

    #User authentication parsers
    password_parser = reqparse.RequestParser()
    password_parser.add_argument(
        'password', type=str, required=True, location='form')

#Custom formators for output fields
class DateTimeFormat(fields.Raw):
    '''Returns utc time_stamp in seconds'''
    def format(self, datetime):
        return get_utc_timestamp(datetime = datetime)

class OutputFields:
    '''Output fields defined for all api endpoints'''
    #Role output fields
    role_fields = {
        'name': fields.String(attribute='title'),
        'id': fields.Integer(attribute='id'),
        'uri': fields.Url('user_endpoint', absolute=True)
    }

    #Basic user output fields
    user_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String,
        'full_name': fields.String(attribute='real_name'),
        'website': fields.String(default=None),
        'bio': fields.String(default=None),
        'created_date': DateTimeFormat(),
        'modified_date': DateTimeFormat(),
        'uri': fields.Url('user_endpoint', absolute=True),
        'role': fields.Nested(role_fields),
        'questions_url': fields.String("NOT_YET_IMPLEMENTED"),
        'answers_url': fields.String("NOT_YET_IMPLEMENTED"),
        'upvoted_questions_url': fields.String("NOT_YET_IMPLEMENTED"),
        'upvoted_answers_url': fields.String("NOT_YET_IMPLEMENTED"),
    }

#Common functions
def user_existance_check(username):
    '''Returns user object if user exists otherwise aborts with 404 status'''
    try:
        user = User.get(username)
        return user
    except ValueError:
        abort(404, error="Username {} doesn't exist".format(username))

def get_private_key(public_key):
    '''Gets clients private key for a corresponding public key'''
    client_secret = app.config["CLIENT_SECRET"]
    if public_key and public_key in client_secret:
        return client_secret[public_key]
    abort(401, error="Unknown Public-Key in HTTP header")

def check_signature(private_key, data):
    '''
    Creates signature and matches with signature passed by client.
    Aborts with 401 status if signature doesn't match
    '''
    signature = data["Signature"]
    expiry = data["Expiry-Time"]

    check_request_expiry(expiry) #Check for valid expiry time

    if not verify_bcrypt_hash(signature, expiry+private_key):
        abort(401, error="Invalid signature")

def check_request_expiry(time_stamp):
    '''
    Checks :
    If the expiry time is expired according to server time aborts with 401 status
    If the expiry time is more than 15 minutes from now then aborts with 400 status
    '''
    if(float(time_stamp) < get_utc_timestamp()):
        abort(401, error = "Expired request")

    if(float(time_stamp) > get_utc_timestamp(15)):
        abort(400, error = "Expiry cannot be more than 15 minutes")

#Decorators
def verify_client(func):
    '''
    Verify whether the client has valid public key or not.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        req_args = Parsers.client_key_parser.parse_args()
        private_key = get_private_key(req_args["Public-Key"])
        return func(*args, **kwargs)
    return wrapper

def client_validate(func):
    '''
    Validates publick_key, signature and expiry time
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        req_args = Parsers.client_key_parser.parse_args()
        private_key = get_private_key(req_args["Public-Key"])
        check_signature(private_key, req_args)
        return func(*args, **kwargs)
    return wrapper

def user_validate(func):
    '''
    Validates publick_key, signature and expiry time
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        print args, kwargs
        return func(*args, **kwargs)
    return wrapper