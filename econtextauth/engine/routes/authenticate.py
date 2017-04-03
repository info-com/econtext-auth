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
        * API passwords are encrypted in our DB, so the input should be
          encrypted appropriately as well to match it
        
        If a user is not a member of the requested application, their
        authentication request should fail, even if their credentials
        are otherwise correct.
        
        Errors should always be generic.  E.g. "Authentication failed"
        rather than "Authentication failed because no matching username
        could be found" or "Authentication failed because the provided
        password did not match"
        
        :param req:
        :param resp:
        :return:
        """
        resp.body = "OK"
        return True
