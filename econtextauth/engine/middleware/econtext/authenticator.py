# -*- encoding: utf-8 -*-

import logging
from econtextauth.models.user.user import User
from argon2 import PasswordHasher
import falcon
import six
import compat

log = logging.getLogger('econtext')


class Authenticator(object):
    def __init__(self, conf):
        self.app_id = conf.get('app_id')
        if self.app_id is None:
            raise Exception("Expected an app_id to authenticate to")
    
    def _decode_basic_auth(self, http_auth):
        """
        Retrieve a username and password from an Authorization header
        
        :param http_auth:
        :return: A username and password
        """
        if isinstance(http_auth, six.string_types):
            http_auth = http_auth.encode('ascii')
        try:
            auth_type, user_and_password = http_auth.split(six.b(' '), 1)
        except ValueError as err:
            msg = "Basic authorize header value not properly formed. Supplied header {0}. Got error: {1}"
            msg = msg.format(http_auth, str(err))
            raise falcon.HTTPUnauthorized('401 Unauthorized', msg, 'Basic realm="eContext Authentication"', href='http://docs.example.com/auth')
        if auth_type.lower() == six.b('basic'):
            user_and_password = compat.decodebytes(user_and_password.strip())
            username, password = user_and_password.split(six.b(':'), 1)
            return username, password
        return
    
    def process_request(self, req, resp):
        try:
            username, password = self._decode_basic_auth(req.auth)
            this_user = User.get(email=username)
            if this_user:
                ph = PasswordHasher()
                ph.verify(this_user.fields.password, password)
                for apps in this_user.fields.applications.all():
                    if apps.fields.id == self.app_id:
                        return True
        except:
            pass
        
        raise falcon.HTTPUnauthorized('401 Unauthorized', "Authentication required", 'Basic realm="eContext Authentication"', href='http://docs.example.com/auth')
