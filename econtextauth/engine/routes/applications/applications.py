import logging
from econtextauth.models.application import application

log = logging.getLogger('econtext')



class Applications:
    """
       Applications
       
       GET  - Retrieve all Applications

    """
    routes = ['applications/applications']
    
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
        show_table = list(application.Application.all())
        log.debug(show_table)
        resp.body = show_table
        return True
