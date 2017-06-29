"""
Basic User object

Should contain the following fields:

id
email
password (hashed)
name
status (ENABLED|UNVERIFIED|DISABLED)
custom_data (a JSON object)
created_at (2017-02-10T21:32:18.042Z)
modified_at (2017-02-10T21:32:18.042Z)
password_modified_at (2017-02-10T21:32:18.042Z)

"""
import logging
import falcon
import bcrypt
from remodel.models import Model, before_save
from validate_email import validate_email
from econtextauth import get_base_url
from econtextauth.models import application, group
from rethinkdb import now
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
            'id': self.get('id'),
            'name': self.get('name'),
            'email': self.get('email'),
            'username': self.get('username'),
            'custom_data': self.get('custom_data'),
            'href': '{}/api/users/user/{}'.format(get_base_url(), self.get('id')),
            'created_at': str(self.get('created_at') or ''),
            'modified_at': str(self.get('modified_at') or ''),
            'status': self.get('status', 'DISABLED'),
            
            # Extra relations
            'apikeys': list(self.fields.api_keys.all()),
            'applications': list(self.fields.applications.all()),
            'groups': list(self.fields.groups.all())
        }
    
    @property
    def json_minimal(self):
        return {  # base user data
            'id': self.get('id'),
            'name': self.get('name'),
            'email': self.get('email'),
            'username': self.get('username'),
            'custom_data': self.get('custom_data'),
            'href': '{}/api/users/user/{}'.format(get_base_url(), self.get('id')),
            'created_at': str(self.get('created_at') or ''),
            'modified_at': str(self.get('modified_at') or ''),
            'status': self.get('status', 'DISABLED')
        }
    
    @staticmethod
    def create_new(email, password, applications, name=None, custom_data=None, status='UNVERIFIED', id_=None, username=None, groups=None, *args, **kwargs):
        """
        Create a new User object
        
        @todo -- We can create password policies associated with an Application and enforce those here
        """
        email = User.check_email(email)
        password = User.check_password(password)
        apps = User.check_applications(applications)
        grps = User.check_groups(groups)
        created_at = now()
        password_modified_at = now()
        
        user = User(
            email=email,
            password=password,
            name=name,
            custom_data=custom_data,
            status=status,
            username=username,
            created_at=created_at,
            password_modified_at=password_modified_at
        )
        if id_ and id_.strip() != '':
            if User.id_already_exists(id_):
                raise falcon.HTTPInvalidParam("A User with that id already exists", 'id')
            user.fields.id = id_
        
        user.save()
        # Add in connected applications and groups
        for app in apps.values():
            user['applications'].add(app)
        for grp in grps.values():
            user['groups'].add(grp)
        user.save()
        return user
    
    def update_model(self, updates=None):
        """
        Updates a User
        
        :return:
        """
        if updates is None:
            return
        
        updates.pop('created_at', None)
        if updates.get('email') and updates['email'] != self.fields.email:
            self.fields.email = User.check_email(updates.pop('email'))
        
        if updates.get('password'):
            self.fields.password = User.check_password(updates.pop('password'))
            self.fields.password_modified_at = now()
        
        if updates.get('applications'):
            apps = User.check_applications(updates.pop('applications'))
            for app in apps.values():
                self['applications'].add(app)
        
        if updates.get('groups'):
            grps = User.check_groups(updates.pop('groups'))
            for grp in grps.values():
                self['groups'].add(grp)
        
        for k, v in updates.items():
            if k in ('name', 'custom_data', 'status'):
                self[k] = v
        
        self.save()
        return self
    
    @before_save
    def update_modification_time(self):
        """
        Update the modified_at parameter whenever we save
        
        :return:
        """
        self.fields.modified_at = now()
        return True
    
    @staticmethod
    def id_already_exists(id_):
        """
        Check to see if a record already exists with this id
        :param id:
        :return:
        """
        if User.get(id_):
            return True
        return False
    
    @staticmethod
    def email_already_exists(email):
        """
        Check to see if a record already exists with this email
        :param email:
        :return boolean:
        """
        if User.get(email=email):
            return True
        return False
    
    @staticmethod
    def check_email(email):
        email = email.lower().strip()
        if User.email_already_exists(email):
            raise falcon.HTTPInvalidParam("A user with that email address already exists", 'email')
        if not validate_email(email):
            raise falcon.HTTPInvalidParam("Invalid email address", 'email')
        return email
    
    @staticmethod
    def check_password(password):
        if len(password.strip()) < 8:
            raise falcon.HTTPInvalidParam("Password must be at least 7 characters long", 'password')
        return bcrypt.hashpw(password.strip().encode('utf8'), bcrypt.gensalt())
    
    @staticmethod
    def check_applications(applications):
        if not isinstance(applications, list):
            raise falcon.HTTPInvalidParam("Expecting a list of application ids", 'applications')
        apps = {}
        for app_id in applications:
            app = application.application.Application.get(app_id)
            if not app:
                raise falcon.HTTPInvalidParam("Couldn't find application {}".format(app_id), 'applications')
            apps[app_id] = app
        return apps
    
    @staticmethod
    def check_groups(groups):
        grps = {}
        if groups:
            if not isinstance(groups, list):
                raise falcon.HTTPInvalidParam("Expecting a list of group ids", 'groups')
            for grp_id in groups:
                grp = group.group.Group.get(grp_id)
                if not grp:
                    raise falcon.HTTPInvalidParam("Couldn't find group {}".format(grp_id), 'groups')
                grps[grp_id] = grp
        return grps
