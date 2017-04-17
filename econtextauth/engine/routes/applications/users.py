import logging
import rethinkdb as r
from econtextauth.models.application import application
from econtextauth.models.user import user

log = logging.getLogger('econtext')


class Users:
    """
    Users

    GET  - Retrieve all users associated with a particular application
    """
    routes = ['applications/application/{appid}/users']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Users(*args)
    
    def on_get(self, req, resp, appid):
        """
        Retrieve all users belonging to an application

        :param req:
        :param resp:
        :return:
        """
        grp = application.Application.get(appid)
        if not grp:
            raise Exception("Application could not be found")
        
        #query = r.table('_group_users').get_all(groupid, index='group_id').eq_join('user_id', r.table('users'),
        #                                                                           index='id').map(lambda x: x['right'])
        users = [a for a in grp.fields.users.all()]
        resp.body = {"users": users}
        return True
