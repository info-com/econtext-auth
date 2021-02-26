import logging
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Users(Route):
    """
        Users
    
        GET  - Retrieve all users
    """
    
    def on_get(self, req, resp):
        """
            Retrieve all users
    
            :param req:
            :param resp:
            :return:
        """
        mapper = self.meta.get('mapper')
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0
        order_by = req.get_param('order_by') or 'email'
        log.debug("limit:    %s", limit)
        log.debug("offset:   %s", offset)
        log.debug("order_by: %s", order_by)
        users = mapper.user.User.get_all(
            organization_flag=True, application_flag=True, group_flag=True, apikey_flag=False,
            limit=limit, offset=offset, order_by=order_by
        )
        if req.get_param('minimal'):
            users = [u.to_dict_minimal() for u in users]
        else:
            users = [u.to_dict() for u in users]
        
        resp.body = {"users": users}
        return True
