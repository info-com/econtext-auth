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
        return {  # base user data
            'id': self.fields.id, 'name': self.fields.name, 'email': self.fields.email,
            'customData': self.fields.customData, 'href': '/api/users/user/{}'.format(self.fields.id),
            
            # Extra relations
            'api_keys': list(self.fields.api_keys.all()), 'groups': self.show_ids(list(self.fields.groups.all())),
            'applications': self.show_ids(list(self.fields.applications.all()))}
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(**kwargs)
    
    @staticmethod
    def create_new(email, password, name=None, custom_data=None, password_modified_at=None, *args, **kwargs):
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
        created_at = r.now()
        modified_at = r.now()
        
        password_modified_at = password_modified_at or r.now()
        # log.debug('typeof name: ',type(name))
        # assert (type(name) is str ), "name is not string type!"
        # assert isinstance(name, str)
        
        
        status = "ENABLED"
        u = User(email=email, password=password, name=name, customData=custom_data, status=status, createdAt=created_at,
                 modifiedAt=modified_at, passwordModifiedAt=password_modified_at)
        
        u.save()
        return u
    
    @staticmethod
    def save_user(update_user, email=None, name=None, password=None, status=None, customData=None, **kwargs):
        """
        Saves a new User object
        
        @todo -- All new users need to be associated with an Application
        @todo -- We can create password policies associated with an Application and enforce those here
        @todo -- Check that an email address is actually an email address (https://pypi.python.org/pypi/validate_email)
        
        :param email:
        :param password:
        :param name:
        :param customData:
        :param status:
        :param passwordModifiedAt:
        :param args:
        :param kwargs:
        :return:
        """
        if kwargs is not None:
            u = update_user
            log.debug(name)
            log.debug(email)
            log.debug(password)
            
            if email != None:
                if email != u['email']:
                    if User.already_exists(email):
                        raise Exception("A user with that email address already exists")
                    if not validate_email(email):
                        raise Exception("Enter a valid email address")
                    u['email'] = email
            
            if password != None:
                
                if len(password.strip()) < 6:
                    raise Exception("Password must be at least 7 characters long")
                ph = PasswordHasher()
                u['password'] = ph.hash(password.strip())
            
            if name != None:
                u['name'] = name
            if status != None:
                u['status'] = status
            if customData != None:
                u['customData'] = customData
            
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
    
    @staticmethod
    def show_ids(idlist):
        returnidlist = []
        for ap in idlist:
            returnidlist.append(ap.fields.id)
        return returnidlist
