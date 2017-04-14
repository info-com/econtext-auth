import logging
from econtextauth.models.user import user
from econtextauth.models.application import application

log = logging.getLogger('econtext')


class Application:
    """
    Application
    
    POST - Add an Application connection to a User
    DELETE - Remove an Application connection from a User
    """
    routes = [
        'users/user/{userid}/application/{appid}'
    ]
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Application(*args)
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    def on_post(self, req, resp, userid, appid):
        """
        Add an Application connection to a user
        :param req:
        :param resp:
        """
        u = user.User.get(userid)
        a = application.Application.get(appid)
        if not u:
            raise Exception('User not found')
        if not a:
            raise Exception('Application not found')
        
        u['applications'].add(a)
        resp.body = True
        return True
    
    def on_delete(self, req, resp, userid, appid):
        """
        Remove an Application connection from a user
        
        :param req:
        :param resp:
        :param userid:
        :param appid:
        :return boolean:
        """
        u = user.User.get(userid)
        a = application.Application.get(appid)
        if not u:
            raise Exception('User not found')
        if not a:
            raise Exception('Application not found')
        
        u['applications'].remove(a)
        resp.body = True
        return True
