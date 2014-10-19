import re
import time
import hashlib
from unicodedata import normalize

from flaq import bcrypt
from flask.ext.login import make_secure_token

#Verify the password hash with the given password
def verify_password(password_hash, password):
    """
    Verify the password hash with the password
    """
    return bcrypt.check_password_hash(password_hash, password)

#Create a password hash using bcrypt
def make_password_hash(password):
    """
    Create a password hash
    """
    return bcrypt.generate_password_hash(password)

#Create proper slugs - https://gist.github.com/turicas/1428479
def slugify(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
    return ''.join(strict_text)

def get_secure_token(*args, **kwargs):
    return make_secure_token(*args, **kwargs)

def get_sha256_hash(string):
    return hashlib.sha256(string).hexdigest()

def get_utc_timestamp(minutes = 0):
    '''return a UNIX style timestamp representing X minutes from now'''
    seconds = minutes * 60
    return int(time.time()+seconds)