import logging
import rethinkdb as r
import falcon
from econtextauth.models.group import group
from econtextauth.models.user import user
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Users(Route):
    """
    Groups
    
    GET  - Retrieve all groups
    """
    
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

        status = req.get_param('status')
        
        query = r.table('_group_users').get_all(groupid, index='group_id').eq_join('user_id', r.table('users'), index='id').map(lambda x: x['right'])
        users = [user.User(**u) for u in query.run()]
        if status:
            users = [u for u in users if u['status'] == status]
        if req.get_param('minimal'):
            users = [u.json_minimal for u in users]
        resp.body = {"users": users}
        return True
