import logging
import falcon
from econtextauth.models.user import user
from econtextauth.models.group import group
log = logging.getLogger('econtext')


class Group:
    """
    Group

    POST - Add a Group connection to a User
    DELETE - Remove a Group connection from a User
    """
    routes = [
        'users/user/{userid}/group/{groupid}'
    ]
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Group(*args)
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    def on_post(self, req, resp, userid, groupid):
        """
        Add a Group connection to a user
        
        :param req:
        :param resp:
        """
        u = user.User.get(userid)
        g = group.Group.get(groupid)
        if not u:
            raise falcon.HTTPInvalidParam('User not found', 'userid')
        if not g:
            raise falcon.HTTPInvalidParam('Group not found', 'groupid')
        
        u_applications = set([a.fields.id for a in u.fields.applications.all()])
        if g['application']['id'] not in u_applications:
            raise falcon.HTTPInvalidParam('User is not a member the application {} specified by this group'.format(g['application']['id']), 'groupid')
        
        u['groups'].add(g)
        resp.body = {"group": True}
        return True
    
    def on_delete(self, req, resp, userid, groupid):
        """
        Remove a Group connection from a user

        :param req:
        :param resp:
        :param userid:
        :param groupid:
        :return boolean:
        """
        u = user.User.get(userid)
        g = group.Group.get(groupid)
        if not u:
            raise falcon.HTTPInvalidParam('User not found', 'userid')
        if not g:
            raise falcon.HTTPInvalidParam('Group not found', 'groupid')
        
        g['users'].remove(u)
        resp.body = {"deleted": True}
        return True
