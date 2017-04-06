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
        if body['type'] == 'username':
            u = User.get(email=body['credential']['email'])
            if u:
                if self.checkPass(u.fields.password, body['credential']['password']):
                    resp.body = "SUCESS"
                    return True
                
                application_list = list(u.fields.applications.all())
                if self.checkForApplication(application_list,body['application']):
                    resp.body = "SUCESS"
                    return True

        if body['type'] == "apikey":
            a=ApiKey.get(body['credential']['secretId'])
        resp.body= "FAIL"
        return False
        

        



    @staticmethod
    def checkPass(bodytext,dbpass):
        ph = PasswordHasher()
        if ph.verify(bodytext,dbpass):
            return True
        return False
    @staticmethod
    def checkForApplication(applist, appid):
        for apps in applist:
            if appid == apps.fields.id:
                return True
        return False