from flaq import app, db, utils, bcrypt
from flaq.utils import verify_password, make_password_hash
from model import User


class UserApi(object):
    """
    Acts as a primary interface for creating and retriving user details.
    """


    def __init__(self, **details):
        """
        Optional user details initializations, Useful when creating the user
        """
        self.username = details.get('username', None)
        self.email = details.get('email', None)
        self.password = details.get('password', '')
        self.real_name = details.get('real_name', '')
        self.website = details.get('website', '')
        self.bio = details.get('bio', '')

    def create(self, **details):
        """
        Create a new user

        :param username: keyword argument [immutable] [required]
        :param email: keyword argument [mutable] [required]
        :param password: keyword argument, plain text password [mutable] [required]
        :param real_name: keyword argument [mutable] [optional]
        :param website: keyword argument [mutable] [optional]
        :param bio: keyword argument [mutable] [optional]

        :returns object: sqlalchemy object

        """

        #Username, password and email are necessary to create a user
        if not (self.username and self.email and self.password):
            raise ValueError('Either username, email or password is empty')
        self.username_exists(self.username) #Raises excpetion if user already exist
        self.email_exists(self.email) #Raises Exception if email alredy exist

        #Create new user
        new_user = User()
        new_user.username = self.username
        new_user.email = self.email
        #Store password hash instead of plain text
        new_user.password = make_password_hash(self.password)
        new_user.real_name = self.real_name
        new_user.website = self.website
        new_user.bio = self.bio
        db.session.add(new_user)
        db.session.commit()

        return new_user

    def delete(self, username):
        """
        Delete a user entry from database, raises exception if user not found

        :param username:

        :returns Integer: primary key(user id) of the deleted user

        """

        user = self.get(username)
        if user:
            db.session.delete(user)
            db.session.commit()
            return user.id
        else:
            raise ValueError('User does not exist')

    def get(self, username_email):
        """
        Get a sqlalchemy db object for a given username or email
        assuming username or emailid is unique for a user and both cannot be similar

        :params username_email: Either username or email

        :returns object or None: sqlalchemy db object or None

        """

        user = db.session.query(User).filter(
            db.or_(User.username == username_email,
                    User.email == username_email)).all()
        return user[0] if user else None

    def get_id(self, username_email):
        """
        Similar to method 'get' instead returns user_id

        :params username_email: Either username or email

        :returns Integer or None:

        """

        return self.get(username_email).id

    def edit(self, username, **details):
        """
        Modifies the user details with given details

        :params username: [required]
        :param email: keyword argument [optional]
        :param password: keyword argument, plain text password [optional]
        :param real_name: keyword argument [optional]
        :param website: keyword argument [optional]
        :param bio: keyword argument [optional]

        :returns object or None: modified sqlalchemy db object or None if no keyword arguments
        :raises ValueError: If username not found
        """

        user = self.get(username)

        if not user:
            raise ValueError('Invalid username')

        if not details:
            return None

        user.email = details.get('email', user.email)
        user.real_name = details.get('real_name', user.real_name)
        user.website = details.get('website', user.website)
        user.bio = details.get('bio', user.bio)

        #Create a password hash for new password
        password = details.get('password')
        if password:
            user.password = make_password_hash(password)

        db.session.commit()
        return user

    def username_exists(self, username):
        """
        Checks whether username exist or not

        :param username:

        :returns Bool(True): If user does not exist
        :raises ValueError: If user exists

        """

        if self.get(username):
            raise ValueError('Username already exists')
        return True

    def email_exists(self, email):
        """
        Checks whether username exist or not

        :param username:

        :returns Bool(True): If user does not exist
        :raises ValueError: If user exists

        """

        if self.get(email):
            raise ValueError('Email alreay exists')
        return True