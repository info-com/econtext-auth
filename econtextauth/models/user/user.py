"""
Basic User object

Should contain the following fields:

id
email
password (hashed)
name
status (ENABLED|DISABLED)
customData (a JSON object)
createdAt (2017-02-10T21:32:18.042Z)
modifiedAt (2017-02-10T21:32:18.042Z)
passwordModifiedAt (2017-02-10T21:32:18.042Z)

"""
import rethinkdb as r
from remodel.models import Model, after_init
from argon2 import PasswordHasher
import logging
from validate_email import validate_email




log = logging.getLogger('econtext')

class User(Model):
    has_and_belongs_to_many = ("Application", "Group")
    has_many = ("ApiKey",)

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            # base user data
            'id': self.fields.id,
            'name': self.fields.name,
            'email': self.fields.email,
            'customData': self.fields.customData,
            
            # Extra relations
            'api_keys': list(self.fields.api_keys.all()),
            'groups': list(self.fields.groups.all()),
            'applications': list(self.fields.applications.all())
        }

    def __init__(self, *args, **kwargs ):
        super(User, self).__init__(**kwargs)
    
    @staticmethod
    def create_new(email, password, name=None, customData=None, status=None, createdAt=None, modifiedAt=None, passwordModifiedAt=None, *args, **kwargs):
        """
        Create a new User object
        
        @todo -- All new users need to be associated with an Application
        @todo -- We can create password policies associated with an Application and enforce those here
        @todo -- Check that an email address is actually an email address (https://pypi.python.org/pypi/validate_email)
        
        :param email:
        :param password:
        :param name:
        :param customData:
        :param status:
        :param createdAt:
        :param modifiedAt:
        :param passwordModifiedAt:
        :param args:
        :param kwargs:
        :return:
        """
        if User.already_exists(email):
            raise Exception("A user with that email address already exists")
        if not validate_email(email):
            raise Exception("Enter a valid email address")
        ph = PasswordHasher()
        if len(password.strip()) < 6:
            raise Exception("Password must be at least 7 characters long")
        password = ph.hash(password.strip())
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        passwordModifiedAt = passwordModifiedAt or r.now()
        u = User(email=email, password=password, name=name, customData=customData, status=status, createdAt=createdAt, modifiedAt=modifiedAt, passwordModifiedAt=passwordModifiedAt)
        u.save()
        return u
    
    @staticmethod
    def already_exists(email):
        """
        Check to see if a record exists already with this email address
        :param email:
        :return boolean:
        """
        if User.get(email=email):
            return True
        return False

    def valid_email(email):
        return validate_email(email)


    # @staticmethod
    # def delete_status():
