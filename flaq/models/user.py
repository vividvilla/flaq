import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from flaq import db
from flaq.utils import verify_password, make_password_hash
from question import Question

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique = True)
    real_name = db.Column(db.String(100))
    website = db.Column(db.String(100))
    bio = db.Column(db.Text)
    role = db.Column(db.Enum('admin', 'mod', 'user', 'banned', name='roles'))
    questions = db.relationship('Question', backref='user', lazy='dynamic')
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)

    def __init__(self, **details):
        self.username = details.get('username', None)
        self.email = details.get('email', None)
        self.password = details.get('password', '')
        self.real_name = details.get('real_name', '')
        self.website = details.get('website', '')
        self.bio = details.get('bio', '')
        self.role = details.get('role', 'user')

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.username)

    def create(self):
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
        self._username_doesnot_exist(self.username) #Raises excpetion if user already exist
        self._email_doesnot_exist(self.email) #Raises Exception if email alredy exist

        #Store password hash instead of plain text
        self.password = make_password_hash(self.password)
        self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()

        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def get(cls, username_email):
        """
        Get a sqlalchemy db object for a given username or email
        assuming username or emailid is unique for a user and both cannot be similar

        :params username_email: Either username or email

        :returns object or None: sqlalchemy db object or None

        """

        try:
            user = cls.query.filter(
                db.or_(cls.username == username_email,
                    cls.email == username_email)).one()
        except MultipleResultsFound as e:
            raise ValueError('Multiple recoreds found, Duplicates in table')
        except NoResultFound as e:
            raise ValueError('User doesnt exist')

        return user

    def delete(self, username):
        """
        Delete a user entry from database, raises exception if user not found

        :param username:

        :returns Integer: primary key(user id) of the deleted user

        """

        user = self.get(username)
        db.session.delete(user)
        db.session.commit()
        return user.id

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

        self.modified_date = datetime.datetime.now()
        db.session.commit()
        return user

    @property
    def user_role(self):
        """
        Get user role

        :params username_email: either username or email

        :returns new user role:
        """

        return self.get(self.username).role

    @user_role.setter
    def user_role(self, role = 'user'):
        """
        Set new user role for a given user

        :params username_email: either username of email
        :params role: role must be any one of the enum value

        :returns new user role:
        """

        user = self.get(self.username)
        user.role = role
        db.session.commit()
        return user.role

    def _username_doesnot_exist(self, username):
        """
        Checks whether username exist or not

        :param username:

        :returns Bool(True): If user does not exist
        :raises ValueError: If user exists

        """

        try:
            self.get(username)
        except ValueError:
            return True
        raise ValueError('Username already exists')

    def _email_doesnot_exist(self, email):
        """
        Checks whether username exist or not

        :param username:

        :returns Bool(True): If user does not exist
        :raises ValueError: If user exists

        """

        try:
            self.get(email)
        except ValueError:
            return True
        raise ValueError('Email already exists')