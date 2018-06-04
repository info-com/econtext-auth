import logging
from econtextauth.models.application import application
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Applications(Route):
    """
       Applications
       
       GET  - Retrieve all Applications

    """
    
    def on_get(self, req, resp):
        """
        Retrieve aall applications

        :param req:
        :param resp:
        :return:
        """
        applications = list(application.Application.all())
        resp.body = {"applications": applications}
        return True
