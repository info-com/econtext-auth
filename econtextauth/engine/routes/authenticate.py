from argon2 import PasswordHasher
from econtextauth.models.user.user import User
import logging
log = logging.getLogger('econtext')


class Authenticate:
    """
    Authenticate
    
    Authenticate against the eContext user store
    """
    routes = [
        'authenticate'
    ]
    
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

                application_list=list(u.fields.applications.all())
                app_check=False
                for apps in application_list:
                    print apps.fields.id
                    if body['application']==apps.fields.id:
                        app_check=True
                if not app_check:
                    resp.body = "FAIL"
                    return False

                ph = PasswordHasher()
                #passcheck=ph.verify(u.fields.password, body['credential']['password'])
                if ph.verify(u.fields.password, body['credential']['password']):
                    resp.body = "SUCESS"
                    return True

        resp.body = "FAIL"
        return False
