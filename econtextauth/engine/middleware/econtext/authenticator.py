# -*- encoding: utf-8 -*-

from econtextauth.models.user import user
import bcrypt
import logging
import basicauth
import falcon

log = logging.getLogger('econtext')


class Authenticator(object):
    def __init__(self, conf):
        self.application_id = conf.get('application_id')
        log.info("System application_id is {}".format(self.application_id))
        if self.application_id is None:
            raise Exception("Expected an application_id to authenticate to")
    
    def process_request(self, req, resp):
        if req.path == '/api/ping':
            return True
        
        log.debug("authenticator.process_request")
        try:
            username, password = basicauth.decode(req.auth)
            u = user.User.get(email=username)
            if u:
                passed = bcrypt.checkpw(password.encode('utf8'), u.fields.password.encode('utf8'))
                if passed:
                    for apps in u.fields.applications.all():
                        if apps.fields.id == self.application_id:
                            return True
        except Exception as e:
            log.debug("Caught an exception during authentication: {}".format(e))
        
        raise falcon.HTTPUnauthorized('401 Unauthorized', "Authentication required", ['Basic realm="eContext Authentication"'])
