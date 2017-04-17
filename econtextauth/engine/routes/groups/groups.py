import logging
from econtextauth.models.group import group

log = logging.getLogger('econtext')


class Groups:
    """
    Groups
    
    GET  - Retrieve all groups
    """
    routes = ['groups']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Groups(*args)
    
    def on_get(self, req, resp):
        """
        Retrieve all groups

        :param req:
        :param resp:
        :return:
        """
        groups = list(group.Group.all())
        resp.body = {"groups": groups}
        return True

