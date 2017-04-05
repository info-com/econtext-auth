# -*- encoding: utf-8 -*-
#
# Copyright 2013 Jay Pipes
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
from econtextauth.models.user.user import User
from argon2 import PasswordHasher
from talons.auth import interfaces

log = logging.getLogger('econtextauth')


class Authenticator(interfaces.Authenticates):
    
    def __init__(self, **conf):
        self.app_id = conf.get('app_id', None)
        if self.app_id is None:
            raise Exception("Expected an app_id to authenticate to")

    def authenticate(self, identity):
        """
        Looks at the supplied identity object and returns True if the
        credentials can be verified, False otherwise.
        """
        # check_password returns None if user was not found...
        u = User.get(identity.login)
        if u:
            ph = PasswordHasher()
            if ph.verify(identity.key, u.fields.password):
                application_list = list(u.fields.applications.all())
                for apps in application_list:
                    log.debug("apps.fields.id: {}".format(apps.fields.id))
                    if self.app_id == apps.fields.id:
                        return True
        
        return False
