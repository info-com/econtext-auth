import logging
from econtext.util.falcon.route import Route
import falcon
log = logging.getLogger('econtextauth')


class Users(Route):
    """
    Users

    GET  - Retrieve all users associated with a particular Organization
    """
    
    def on_get(self, req, resp, orgid):
        """
        Retrieve all users belonging to an Organization

        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.organization.Organization.get_by_uid(orgid, user_flag=True)
        if not o:
            raise falcon.HTTPInvalidParam("Organization could not be found", orgid)
        
        users = sorted([u.to_dict_minimal() for u in o.users], key=lambda x: x['username'])
        
        resp.body = {"users": users}
        return True
