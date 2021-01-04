import logging
from econtext.util.falcon.route import Route
log = logging.getLogger('econtextauth')


class Organizations(Route):
    """
       Organizations
       
       GET  - Retrieve all Organizatsions

    """
    
    def on_get(self, req, resp):
        """
        Retrieve all organizations

        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0
        order_by = req.get_param('order_by') or 'name'
        organizations = [
            a.to_dict_minimal() for a in mapper.organization.Organization.get_all(limit=limit, offset=offset, order_by=order_by)
        ]
        resp.body = {"organizations": organizations}
        return True
