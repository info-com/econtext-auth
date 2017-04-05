# -*- encoding: utf-8 -*-

import logging
from econtextauth.models.user.user import User
from argon2 import PasswordHasher
import falcon

#appid vs fields.id
log = logging.getLogger('econtextauth')
admin_userid='70706e44-b263-4f80-b72a-f296ea1e24e4'
admin_appid='f43ddadc-1493-4fc1-8d30-be1dfbc25dbc'


class Authenticator(object):

    def __init__(self, **conf):
        self.app_id = conf.get('app_id', 'f43ddadc-1493-4fc1-8d30-be1dfbc25dbc')
        if self.app_id is None:
            raise Exception("Expected an app_id to authenticate to")

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        account_id = req.get_header('Account-ID')
        #print account_id

        challenges = ['Token type="Fernet"']
        this_user=User.get(admin_userid)
        if this_user:

            application_list = list(this_user.fields.applications.all())
            app_check = False
            for apps in application_list:
                print apps.fields.id
                if apps.fields.id == self.app_id:
                    app_check=True
            if not app_check:
                description = ('Please provide an auth token '
                               'as part of the request.')
                raise falcon.HTTPUnauthorized('Auth token required',
                                              description,
                                              challenges,
                                              href='http://docs.example.com/auth')
            else:
                print 'Authorized'
                return True





