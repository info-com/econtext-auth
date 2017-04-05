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
import os
from econtextauth.models.user.user import User
from talons import exc
from argon2 import PasswordHasher
from talons.auth import interfaces

LOG = logging.getLogger(__name__)

#put in config file...
admin_id='f43ddadc-1493-4fc1-8d30-be1dfbc25dbc'



class Authenticator(interfaces.Authenticates):


    """
    Authenticates the supplied Identity by querying an Apache htpasswd file.
    """
    #
    # def __init__(self, **conf):
    #     """
    #     Construct a concrete object with a set of keyword configuration
    #     options.
    #     :param **conf:
    #         htpasswd_path: Path to the Apache htpasswd file.
    #     :raises `talons.exc.BadConfiguration` if configuration options
    #             are not valid or conflict with each other.
    #     """
    #     htpath = conf.pop('htpasswd_path', None)
    #     if not htpath:
    #         msg = ("Missing required htpasswd_path "
    #                "configuration option.")
    #         LOG.error(msg)
    #         raise exc.BadConfiguration(msg)
    #
    #     if not os.path.exists(htpath):
    #         msg = "htpasswd file {0} does not exist.".format(htpath)
    #         LOG.error(msg)
    #         raise exc.BadConfiguration(msg)
    #
    #     self.htfile = apache.HtpasswdFile(htpath)

    def authenticate(self, identity):
        """
        Looks at the supplied identity object and returns True if the
        credentials can be verified, False otherwise.
        """
        # check_password returns None if user was not found...
        print identity.login , identity.key
        app_check = False
        u = User.get(identity.login)
        if u:
            ph = PasswordHasher()
            # passcheck=ph.verify(u.fields.password, body['credential']['password'])
            if ph.verify(u.fields.password, identity.key):
                application_list = list(u.fields.applications.all())
                for apps in application_list:
                    print apps.fields.id
                    if admin_id == apps.fields.id:
                        app_check = True

        if app_check:
            return True

        return False
        #return self.htfile.check_password(identity.login, identity.key) is True