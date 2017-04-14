from econtextauth.models.user import user
import logging

log = logging.getLogger('econtext')


class Users:
    """
        Users
    
        GET  - Retrieve all users
    """
    routes = ['users']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args):
        return Users(*args)
    
    def on_get(self, req, resp):
        """
            Retrieve all users
    
            :param req:
            :param resp:
            :param userid:
            :return:
        """
        users = list(user.User.all())
        resp.body = users
        return True
