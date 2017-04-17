from argon2 import PasswordHasher
from econtextauth.models.user.user import User
from econtextauth.models.user.apikey import ApiKey
import logging

log = logging.getLogger('econtext')


class Authenticate:
    """
    Authenticate
    
    Authenticate against the eContext user store
    """
    routes = ['authenticate']
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Authenticate(*args)
    
    def __init__(self, options):
        self.options = options
    
    def on_post(self, req, resp):
        """
        Authenticate a user given a set of credentials.  We expect to
        receive a couple of items here:
        
        {
            "type": "username" | "apikey",
            "credential": {
                "username": "USERNAME",
                "password": "PASSWORD"
            },
            "application": "APPLICATION"
        }
        
        * Passwords are hashed in our DB, so the input should be hashed
          appropriately as well to match it
        
        If a user is not a member of the requested application, their
        authentication request should fail, even if their credentials
        are otherwise correct.
        
        Errors should always be generic.  E.g. "Authentication failed"
        rather than "Authentication failed because no matching username
        could be found" or "Authentication failed because the provided
        password did not match"
        
        General method here:
        * Search for the user based on the provided username
        * If there are no matching users -> Fail
        * Check the provided password against the hashed password (use
          ph.verify(user.password, supplied_credential)
        * If there is no match -> Fail
        * Success
        
        :param req:
        :param resp:
        :return:
        """
        body = req.context['body']
        
        try:
            hashed_password = None
            u = None
            
            if body['type'] == 'username':
                u = User.get(email=body['credential']['username'])
                hashed_password = u.fields.password
            
            elif body['type'] == "apikey":
                a = ApiKey.get(body['credential']['username'])
                if Authenticate.check_status(a):
                    hashed_password = a.fields.secret
                    u = a.fields.user
            
            if not Authenticate.check_status(u):
                raise Exception()
            if not Authenticate.check_pass(hashed_password, body['credential']['password']):
                raise Exception()
            
            applications = set([app.fields.id for app in u.fields.applications.all()])
            if body['application'] not in applications:
                raise Exception()
            
            resp.body = {"authenticated": True}
        except Exception as e:
            log.exception(e)
            resp.body = {"authenticated": False}
        
        return True
    
    @staticmethod
    def check_status(item):
        """
        Checks the status field for the object, and returns False if
        the object doesn't exist or if the status equals DISABLED
        
        :param item:
        :return:
        """
        status = item.get('status')
        if not status or str(status).upper() == 'DISABLED':
            return False
        return True
    
    @staticmethod
    def check_pass(hashed_password, unhashed_password):
        if not hashed_password or not unhashed_password.strip():
            return False
        ph = PasswordHasher()
        try:
            ph.verify(hashed_password, unhashed_password)
        except:
            return False
        return True
