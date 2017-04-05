# -*- encoding: utf-8 -*-

import logging
from econtextauth.models.user.user import User
from argon2 import PasswordHasher
import falcon
from falcon import api_helpers
import six
import compat

# appid vs fields.id
log = logging.getLogger('econtext')


class Authenticator(object):
    def __init__(self, conf):
        self.app_id = conf.get('app_id')
        if self.app_id is None:
            raise Exception("Expected an app_id to authenticate to")

    def process_request(self, req, resp):

        http_auth = req.auth
        log.debug(http_auth)
        if isinstance(http_auth, six.string_types):
            http_auth = http_auth.encode('ascii')
        try:
            auth_type, user_and_key = http_auth.split(six.b(' '), 1)
        except ValueError as err:
            msg = ("Basic authorize header value not properly formed. "
                   "Supplied header {0}. Got error: {1}")
            msg = msg.format(http_auth, str(err))
            log.debug(msg)
            return False
        if auth_type.lower() == six.b('basic'):
            user_and_key = user_and_key.strip()
            user_and_key = compat.decodebytes(user_and_key)
            user_id, key = user_and_key.split(six.b(':'), 1)

            log.debug(user_id)
            log.debug(key)

        log.debug(user_and_key)
        log.debug(self.app_id)
        app_check = False

        this_user = User.get(email=user_id)
        if this_user:
            ph = PasswordHasher()

            try:
                ph.verify(this_user.fields.password, key)
                application_list = list(this_user.fields.applications.all())

                for apps in application_list:
                    log.debug(apps.fields.id)
                    if apps.fields.id == self.app_id:
                        return True
            except:
                pass
        description = ('Username or password didnt match')
        raise falcon.HTTPUnauthorized('Username / Password mistmatch',
                                      description,
                                      'Token type="Fernet"',
                                      href='http://docs.example.com/auth')
