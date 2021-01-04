import logging
from econtext.util.falcon.route import Route
log = logging.getLogger('econtextauth')


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
        mapper = self.meta.get('mapper')
        applications = [a.to_dict() for a in mapper.application.Application.get_all()]
        resp.body = {"applications": applications}
        return True
