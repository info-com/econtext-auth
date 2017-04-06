import logging

log = logging.getLogger('econtext')
from econtextauth.models.user import user


class Users:
    routes = ['users/users']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Users(*args)
    
    def on_get(self, req, resp):
        show_table = list(user.User.all())
        log.debug(show_table)
        resp.body = show_table
        return True

