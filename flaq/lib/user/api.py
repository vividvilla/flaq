from flaq import app, db, utils
from model import User

class UserApi(object):

    def __init__(self, **details):
        self.username = details.get("username", None)
        self.email = details.get("email", None)
        self.real_name = details.get("real_name", '')
        self.website = details.get("website", '')
        self.bio = details.get("bio", '')

    def create(self, **details):
        if not (self.username and self.email):
            raise ValueError("Either username or email is empty")

        if self.username_exists(self.username):
            raise ValueError("Username already exists")

        if self.email_exists(self.email):
            raise ValueError("Email already exists")

        new_user = User()
        new_user.username = self.username
        new_user.email = self.email
        new_user.real_name = self.real_name
        new_user.website = self.website
        new_user.bio = self.bio
        db.session.add(new_user)
        db.session.commit()

    def delete(self, username):
        user = self.get(username = username)
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            raise ValueError("User does not exist")

    def get(self, username = False, email = False):
        if username:
            return db.session.query(User).filter_by(username = username).first()
        elif email:
            return db.session.query(User).filter_by(email = email).first()
        else:
            return None

    def get_id(self, username = False, email = False):
        if username:
            return self.get(username = username).id
        elif email:
            return self.get(email = email).id
        else:
            return None

    def edit(self, user_id, **details):
        pass

    def username_exists(self, username):
        return self.get(username = username)

    def email_exists(self, email):
        return self.get(email = email)