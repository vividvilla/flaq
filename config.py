import os

basedir = os.path.abspath(os.path.dirname(__file__))

#Database settings
DB = {
    "host": "localhost",
    "db": "flaq",
    "username": "postgres",
    "password": "postgres"
}

#Flask and flask plugin settings
SECRET_KEY = 'XLGNKFkb7B'
WTF_CSRF_SECRET_KEY = 'XLGNKFkb7B'
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@localhost/{database}'.format(
    username = DB['username'],
    password = DB['password'],
    database = DB['db'])