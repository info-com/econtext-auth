import logging
from econtext.util.falcon.route import Route
log = logging.getLogger('econtext')


class Application(Route):
    """
    User

    GET  - Retrieve a User
    POST - Create a new User
    PUT  - Update a User
    DELETE - Remove a User
    """
    
    def on_post(self, req, resp, userid, appid):
        """
        Attach an application to a user
        
        :param userid:
        :param appid:
        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.user.User.get_by_uid(userid)
        a = mapper.application.Application.get_by_uid(appid)
        
        if not o:
            raise Exception('User %s not found' % userid)
        if not a:
            raise Exception('Application %s not found' % appid)
        
        o = mapper.user.User.attach_application(o, a)
        
        resp.body = {"application": True}
        return True
    
    def on_delete(self, req, resp, userid, appid):
        """
        Detach an Application from a User

        :param req:
        :param resp:
        :param userid:
        :param appid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.user.User.get_by_uid(userid)
        a = mapper.application.Application.get_by_uid(appid)
        
        if not o:
            raise Exception('User %s not found' % userid)
        if not a:
            raise Exception('Application %s not found' % appid)
        
        mapper.user.User.detach_application(o, a)
        resp.body = {"deleted": True}
        return True
