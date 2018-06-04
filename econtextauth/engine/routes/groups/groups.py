import logging
from econtextauth.models.group import group
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Groups(Route):
    """
    Groups
    
    GET  - Retrieve all groups
    """
    
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

