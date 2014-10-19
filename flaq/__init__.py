from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext import restful
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
rest_api = restful.Api(app)
login_manager = LoginManager(app)

#APi routing
from flaq.api.v1 import user

rest_api.add_resource(user.UserApi, '/<string:username>/', endpoint = 'user_endpoint')