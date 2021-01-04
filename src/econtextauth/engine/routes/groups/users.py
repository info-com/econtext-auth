import logging
from econtext.util.falcon.route import Route
import falcon
log = logging.getLogger('econtextauth')


class Users(Route):
    """
    Users

    GET  - Retrieve all users associated with a particular Group
    """
    
    def on_get(self, req, resp, groupid):
        """
        Retrieve all users belonging to an Group

        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.group.Group.get_by_uid(groupid, user_flag=True)
        if not o:
            raise falcon.HTTPInvalidParam("Group could not be found", groupid)
        
        users = [u.to_dict_minimal() for u in o.users]
        
        resp.body = {"users": users}
        return True
