# -*- encoding: utf-8 -*-

import logging
from econtextauth.models.user.user import User
from argon2 import PasswordHasher
import falcon
from falcon import api_helpers

# appid vs fields.id
log = logging.getLogger('econtext')


class Authenticator(object):
    def __init__(self, conf):
        self.app_id = conf.get('app_id')
        if self.app_id is None:
            raise Exception("Expected an app_id to authenticate to")

    def process_request(self, req, resp):
        username = req.get_header('Username')
        password = req.get_header('Password')
        log.debug('username: ', username, 'password: ', password)
        log.debug(self.app_id)

        app_check = False

        this_user = User.get(email=username)
        if this_user:
            ph = PasswordHasher()

            try:
                ph.verify(this_user.fields.password, password)
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
