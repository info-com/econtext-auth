from econtext.util.falcon.route import Route
from jose import jwt
import datetime
import json
from econtext.util.log import log

from ...util import compare_passwords, hash_secret


class Authenticate(Route):
    """
    Authenticate
    
    Authenticate against the Auth user store
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
          appropriately as well to match it after receiving it
        
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
        mapper = self.meta['mapper']
        auth_cache = self.meta['auth_cache']
        
        body = req.context['body']
        type = body['type']
        username = body['credential']['username']
        password = body['credential']['password']
        application_id = body['application']
        ip_address = body.get("ip_address")
        
        try:
            if auth_cache and not auth_cache.check_auth(type, username, password, ip_address):
                raise Exception("Failed in auth_cache check")
            
            hashed_password = None
            u = None
            access_token = None
            
            if type == 'username':
                u = mapper.user.User.get_by_username(username, organization_flag=True, application_flag=True, group_flag=True, apikey_flag=True)
                hashed_password = u.password
            
            elif type == "apikey":
                a = mapper.apikey.ApiKey.get_by_key(username)
                # if the ApiKey is not ENABLED ...
                if not Authenticate.check_status(a):
                    raise Exception("Failed check_status")
                # else, grab the password and populate the User
                hashed_password = a.secret
                u = mapper.user.User.get_by_uid(a.user.uid, organization_flag=True, application_flag=True, group_flag=True, apikey_flag=True)
            
            # if user is not ENABLED ...
            if not Authenticate.check_status(u):
                raise Exception("Failed check_status")
            
            # Check the credentials ...
            if not Authenticate.check_pass(password, hashed_password):
                log.debug("check_pass(%s, %s)", password.encode('utf8'), hashed_password.encode('utf8'))
                log.debug("entered password hash: %s", hash_secret(password.encode('utf8')))
                raise Exception("Failed check_pass")
            
            applications = {app.uid: app for app in u.applications if app.status != 'DISABLED'}
            if application_id not in applications:
                raise Exception("Application not found or not ENABLED")
            
            access_token = Authenticate.build_access_token(u, applications.get(application_id))
            
            resp.body = {"authenticated": True, "user": u.to_dict(), "access_token": access_token}
        
        except Exception as e:
            log.exception("Authentication Failure...")
            log.debug("authentication failed: %s", json.dumps(body))
            if auth_cache:
                auth_cache.add_credential(type, username, password, ip_address)
            resp.body = {"authenticated": False, "user": None, "access_token": None}
        
        return True
    
    @staticmethod
    def check_status(o):
        """
        Checks the status field for the object, and returns False if
        the object doesn't exist or if the status isn't DISABLED
        
        :param o:
        :return:
        """
        return o.status and str(o.status).upper() != 'DISABLED'
    
    @staticmethod
    def check_pass(unhashed_password, hashed_password):
        if not hashed_password or not unhashed_password.strip():
            return False
        try:
            passed = compare_passwords(unhashed_password.strip(), hashed_password)
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
        secret = a.jwt_secret.strip()
        log.debug("building JWT with secret: %s", secret)
        if secret:
            now = datetime.datetime.utcnow()
            tomorrow = now + datetime.timedelta(days=1)
            iss = 'https://auth.econtext.com/api/authenticate'
            groups = [g.name for g in u.groups if g.application == a.uid]
            org_data = {'organization_id': u.organization.uid, 'name': u.organization.name}
            name = u.name
            
            claims = {
                'exp': int(tomorrow.timestamp()),   # tomorrow
                'nbf': int(now.timestamp()),        # now
                'iat': int(now.timestamp()),        # now
                'iss': iss,                         # URL for auth
                'sub': u.uid,                 # user id
                'aud': a.uid,                 # target application,
                'groups': groups,
                'name': name,
                'org': org_data
            }
            access_token = jwt.encode(
                claims,
                secret,
                algorithm='HS256'
            )
        
        return access_token
