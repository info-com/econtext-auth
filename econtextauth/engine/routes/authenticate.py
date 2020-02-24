from econtextauth.models.user.user import User
from econtextauth.models.user.apikey import ApiKey
import bcrypt
from econtext.util.falcon.route import Route
from jose import jwt
import datetime
from econtext.util.log import log


class Authenticate(Route):
    """
    Authenticate
    
    Authenticate against the eContext user store
    """
    
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
        type = body['type']
        username = body['credential']['username']
        password = body['credential']['password']
        ip_address = body.get("ip_address")
        if not self.meta['auth_cache'].check_auth(type, username, password, ip_address):
            raise Exception("Failed in auth_cache check")
        
        try:
            hashed_password = None
            u = None
            access_token = None
            
            if body['type'] == 'username':
                u = User.get(email=body['credential']['username'])
                hashed_password = u.fields.password
            
            elif body['type'] == "apikey":
                a = ApiKey.get(body['credential']['username'])
                if Authenticate.check_status(a):
                    hashed_password = a.fields.secret
                    u = a.fields.user
            
            if not Authenticate.check_status(u):
                self.meta['auth_cache'].add_credential(type, username, password, ip_address)
                log.debug("Failed check_status")
                raise Exception()
            if not Authenticate.check_pass(hashed_password.encode('utf8'), body['credential']['password'].encode('utf8')):
                self.meta['auth_cache'].add_credential(type, username, password, ip_address)
                log.debug("Failed check_pass")
                raise Exception("Failed check_pass")
            
            applications = {app.fields.id: app for app in u.fields.applications.all() if app.get('status') != 'DISABLED'}
            if body['application'] not in applications:
                raise Exception()
            
            access_token = Authenticate.build_access_token(u, applications.get(body['application']))
            
            resp.body = {"authenticated": True, "user": u, "access_token": access_token}
        except Exception as e:
            log.exception(e)
            resp.body = {"authenticated": False, "user": None}
        
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
        try:
            passed = bcrypt.checkpw(unhashed_password, hashed_password)
        except Exception as e:
            log.debug("some error occurred: {}".format(e))
            return False
        return passed
    
    @staticmethod
    def build_access_token(u, a):
        """
        Build an access_token with a set of claims describing the user.
        
        :param u: User
        :param a: Application
        :return: An access token object
        """
        access_token = None
        secret = a.get('jwt_secret', '').strip()
        if secret:
            now = datetime.datetime.utcnow()
            tomorrow = now + datetime.timedelta(days=1)
            iss = 'https://auth.econtext.com/api/authenticate'
            groups = [g.get('name') for g in u.fields.groups.all() if g['application']['id'] == a.fields.id]
            name = u.fields.name
            
            claims = {
                'exp': int(tomorrow.timestamp()),   # tomorrow
                'nbf': int(now.timestamp()),        # now
                'iat': int(now.timestamp()),        # now
                'iss': iss,                         # URL for auth
                'sub': u.get('id'),                 # user id
                'aud': a.get('id'),                 # target application,
                'groups': groups,
                'name': name
            }
            access_token = jwt.encode(
                claims,
                secret,
                algorithm='HS256'
            )
        
        return access_token
