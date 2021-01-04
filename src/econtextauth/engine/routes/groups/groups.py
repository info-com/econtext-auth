import logging
from econtext.util.falcon.route import Route
log = logging.getLogger('econtextauth')


class Groups(Route):
    """
       Groups
       
       GET  - Retrieve all Groups

    """
    
    def on_get(self, req, resp):
        """
        Retrieve all Groups

        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        groups = [a.to_dict() for a in mapper.group.Group.get_all()]
        resp.body = {"groups": groups}
        return True
