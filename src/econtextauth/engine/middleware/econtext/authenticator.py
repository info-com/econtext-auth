# -*- encoding: utf-8 -*-

import logging
import basicauth
import falcon
from ....util import compare_passwords

log = logging.getLogger('econtext')


class Authenticator(object):
    def __init__(self, mapper, application_id):
        self.mapper = mapper
        self.application_id = application_id
        log.info("System application_id is {}".format(self.application_id))
        if self.application_id is None:
            raise Exception("Expected an application_id to authenticate to")
    
    def process_request(self, req, resp):
        if req.path == '/api/ping':
            return True
        
        log.debug("authenticator.process_request")
        try:
            username, password = basicauth.decode(req.auth)
            u = self.mapper.user.User.get_by_username(username, application_flag=True)
            if u:
                log.debug("checking %s: %s", username, password)
                log.debug("against  %s: %s", password, u.password)
                user_applications = {a.uid for a in u.applications}
                if all((self.application_id in user_applications, compare_passwords(password, u.password))):
                    return True
        except Exception as e:
            log.debug("Caught an exception during authentication: {}".format(e))
        
        raise falcon.HTTPUnauthorized('401 Unauthorized', "Authentication required", ['Basic realm="eContext Authentication"'])
