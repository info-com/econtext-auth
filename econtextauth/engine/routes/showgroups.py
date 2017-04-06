import logging

log = logging.getLogger('econtext')
from econtextauth.models.group import group


class Showgroups:
    routes = ['showgroups']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Showgroups(*args)
    
    def on_get(self, req, resp):
        show_table = list(group.Group.all())
        log.debug(show_table)
        resp.body = show_table
        return True

