import logging
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Group(Route):
    """
    User Groups

    POST - Attach a Group to a User
    DELETE - Remove a Group from a User
    """
    
    def on_post(self, req, resp, userid, groupid):
        """
        Attach a group to a user

        :param userid:
        :param groupid:
        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.user.User.get_by_uid(userid)
        g = mapper.group.Group.get_by_uid(groupid)
        
        if not o:
            raise Exception('User %s not found' % userid)
        if not g:
            raise Exception('Group %s not found' % groupid)
        
        o = mapper.user.User.attach_group(o, g)
        resp.body = {"group": True}
        return True
    
    def on_delete(self, req, resp, userid, groupid):
        """
        Detach a Group from a User

        :param req:
        :param resp:
        :param userid:
        :param groupid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.user.User.get_by_uid(userid)
        a = mapper.group.Group.get_by_uid(groupid)
        
        if not o:
            raise Exception('User %s not found' % userid)
        if not a:
            raise Exception('Group %s not found' % groupid)
        
        mapper.user.User.detach_group(o, a)
        resp.body = {"deleted": True}
        return True
