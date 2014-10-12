import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from flaq import db
from flaq.utils import verify_password, make_password_hash
from question import Question

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(1000), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    real_name = db.Column(db.String(100))
    website = db.Column(db.String(100))
    bio = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    questions = db.relationship('Question', backref='user', lazy='dynamic')
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)

    def __init__(self, username, **details):
        self.username = username
        self.email = details.get('email', None)
        self.password = details.get('password', '')
        self.real_name = details.get('real_name', '')
        self.website = details.get('website', '')
        self.bio = details.get('bio', '')
        self.user_role = details.get('role', 'user')

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

        self._username_doesnot_exist(self.username) #Raises excpetion if user already exist
        self._email_doesnot_exist(self.email) #Raises Exception if email alredy exist

        #Store password hash instead of plain text
        self.password = make_password_hash(self.password)
        self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()

        #Set user role
        self.role = self.user_role
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

    def delete(self):
        """
        Delete a user entry from database, raises exception if user not found

        :param username:

        :returns Integer: primary key(user id) of the deleted user

        """

        user = cls.get(self.username)
        db.session.delete(user)
        db.session.commit()
        return user.id

    def edit(self, **newdetails):
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

        user = self.get(self.username)

        if not user:
            raise ValueError('Invalid username')

        if not newdetails:
            return None

        user.email = newdetails.get('email', user.email)
        user.real_name = newdetails.get('real_name', user.real_name)
        user.website = newdetails.get('website', user.website)
        user.bio = newdetails.get('bio', user.bio)

        #Create a password hash for new password
        password = newdetails.get('password')
        if password:
            user.password = make_password_hash(password)

        self.modified_date = datetime.datetime.now()
        db.session.commit()
        return user

    @property
    def role(self):
        """
        Get user role

        :params username_email: either username or email

        :returns new user role:
        """
        return Role.get(self.get(self.username).role_id)

    @role.setter
    def role(self, role = 'user'):
        """
        Set new user role for a given user

        :params username_email: either username of email
        :params role: role must be any one of the enum value

        :returns new user role:
        """
        return Role(role, self.get(self.username)).set_role()

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

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False, unique = True)
    user = db.relationship('User', backref = 'user', lazy = 'dynamic')

    def __init__(self, title, user = None):
        self.title = title
        self.user = user

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get(cls, title_or_id):
        _filter = cls.id if type(title_or_id) == int else cls.title

        try:
            role = cls.query.filter(_filter == title_or_id).one()
        except NoResultFound as e:
            raise ValueError('Role doesnot exist, please crate one before assigning')
        return role

    def set_role(self):
        role = cls.get(self.title)
        role.user.append(self.user)
        db.session.commit()
        return role