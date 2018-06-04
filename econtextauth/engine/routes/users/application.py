import logging
import falcon
import rethinkdb as r
from econtextauth.models.user import user
from econtextauth.models.application import application
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Application(Route):
    """
    Application
    
    POST - Add an Application connection to a User
    DELETE - Remove an Application connection from a User
    """
    
    def on_post(self, req, resp, userid, appid):
        """
        Add an Application connection to a user
        :param req:
        :param resp:
        """
        u = user.User.get(userid)
        a = application.Application.get(appid)
        if not u:
            raise falcon.HTTPInvalidParam('User not found', 'userid')
        if not a:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        
        u['applications'].add(a)
        resp.body = {"application": True}
        return True
    
    def on_delete(self, req, resp, userid, appid):
        """
        Remove an Application connection from a user
        
        :param req:
        :param resp:
        :param userid:
        :param appid:
        :return boolean:
        """
        u = user.User.get(userid)
        a = application.Application.get(appid)
        if not u:
            raise falcon.HTTPInvalidParam('User not found', 'userid')
        if not a:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        
        if u['applications'].count() == 1:
            raise falcon.HTTPConflict('409 Conflict', 'A User must be associated with at least one Application')

        query = r.table('_application_users').get_all(userid, index='user_id').filter({'application_id': appid}).delete().run()
        resp.body = {"deleted": True}
        return True
