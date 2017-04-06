import logging

log = logging.getLogger('econtext')
from econtextauth.models.application import application


class Showapplications:
    routes = ['showapplications']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Showapplications(*args)
    
    def on_get(self, req, resp):
        show_table = list(application.Application.all())
        log.debug(show_table)
        resp.body = show_table
        return True

