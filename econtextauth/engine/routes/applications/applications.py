import logging
from econtextauth.models.application import application

log = logging.getLogger('econtext')


class Applications:
    """
       Applications
       
       GET  - Retrieve all Applications

    """
    routes = ['applications']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Applications(*args)
    
    def on_get(self, req, resp):
        """
        Retrieve aall applications

        :param req:
        :param resp:
        :return:
        """
        applications = list(application.Application.all())
        resp.body = applications
        return True
