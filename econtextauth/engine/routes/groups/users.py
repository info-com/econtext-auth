import logging
import rethinkdb as r
import falcon
from econtextauth.models.group import group
from econtextauth.models.user import user

log = logging.getLogger('econtext')


class Users:
    """
    Groups
    
    GET  - Retrieve all groups
    """
    routes = ['groups/group/{groupid}/users']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Users(*args)
    
    def on_get(self, req, resp, groupid):
        """
        Retrieve all users belonging to a group
        
        :param req:
        :param resp:
        :return:
        """
        grp = group.Group.get(groupid)
        if not grp:
            raise falcon.HTTPInvalidParam("Group could not be found", 'groupid')
        
        query = r.table('_group_users').get_all(groupid, index='group_id').eq_join('user_id', r.table('users'), index='id').map(lambda x: x['right'])
        users = [user.User(**u) for u in query.run()]
        resp.body = {"users": users}
        return True