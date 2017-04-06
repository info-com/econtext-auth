"""
Basic User object

Should contain the following fields:

id
email
password (hashed)
name
href
status (ENABLED|DISABLED)
customData (a JSON object)
createdAt (2017-02-10T21:32:18.042Z)
modifiedAt (2017-02-10T21:32:18.042Z)
passwordModifiedAt (2017-02-10T21:32:18.042Z)

"""
import rethinkdb as r
from remodel.models import Model
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
            'href': '/api/users/user/{}'.format(self.fields.id),
            
            # Extra relations
            #pluck group.id app.id, ONLY SHOW LIST OF ID's
            'api_keys': list(self.fields.api_keys.all()),
            'groups': list(self.fields.groups.all()),
            'applications': list(self.fields.applications.all())
        }

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(**kwargs)

    @staticmethod
    def create_new(email, password, name=None, custom_data=None, status=None, created_at=None, modified_at=None, password_modified_at=None, *args, **kwargs):
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
        created_at = created_at or r.now()
        modified_at = modified_at or r.now()
        password_modified_at = password_modified_at or r.now()
        assert (type(name) is str ), "name is not string type!"
        #assert isinstance(name, str)

        status = "ENABLED"
        u = User(email=email, password=password, name=name, customData=custom_data, status=status, createdAt=created_at,
                 modifiedAt=modified_at, passwordModifiedAt=password_modified_at)
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

    @staticmethod
    def valid_email(email):
        return validate_email(email)
