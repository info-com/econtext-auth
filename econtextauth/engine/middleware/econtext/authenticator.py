# -*- encoding: utf-8 -*-

import logging
from econtextauth.models.user.user import User
from argon2 import PasswordHasher
import falcon

#appid vs fields.id
log = logging.getLogger('econtextauth')




class Authenticator(object):

    def __init__(self,conf):
        self.app_id = conf.get('app_id')
        if self.app_id is None:
            raise Exception("Expected an app_id to authenticate to")

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        username = req.get_header('Username')
        password=req.get_header('Password')
        print 'username: ', username , 'password: ', password
        print self.app_id



        app_check = False
        challenges = ['Token type="Fernet"']
        this_user=User.get(email=username)
        if this_user:
            ph = PasswordHasher()
            if ph.verify(this_user.fields.password, password):
                application_list = list(this_user.fields.applications.all())

                for apps in application_list:
                    print apps.fields.id
                    if apps.fields.id == self.app_id:
                        app_check=True





        print app_check
        #     if not app_check:
        #         description = ('Please provide an auth token '
        #                        'as part of the request.')
        #         raise falcon.HTTPUnauthorized('Auth token required',
        #                                       description,
        #                                       challenges,
        #                                       href='http://docs.example.com/auth')
        #
        # return True





