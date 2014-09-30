from app import app
from app import db
from app.model import User
from app import utils

class User(object):

    def __init__(self, **details):
        self.username = details.get("username", None)
        self.email = details.get("username", None)
        self.real_name = details.get("real_name", '')
        self.website = details.get("website", '')
        self.bio = details.get("bio", '')

    def create(self, **details):
        if not (self.username and self.email):
            raise

        if username_exists(self.username):
            raise

        if email_exists(self.email):
            raise

        new_user = User()
        new_user.username = self.username
        new_user.email = self.email
        new_user.real_name = self.real_name
        new_user.website = self.website
        new_user.bio = self.bio
        db.session.add(new_user)
        db.session.commit()

        return get_user_id(username = self.username)

    def delete(self, username):
        pass

    def get(self, username = False, email = False):
        if username:
            return db.session.query().filter_by(username = username).first()
        elif email:
            return db.session.query().filter_by(username = username).first()
        else:
            return None

    def get_id(self, **details):
        if username:
            return get(username = username).id
        elif email:
            return get(email = email).id
        else:
            return None

    def edit(self, user_id, **details):
        pass

    def username_exists(self, username):
        return get(username = username)

    def email_exists(self, email):
        return get(email = email)