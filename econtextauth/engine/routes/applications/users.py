import logging
from econtextauth.models.application import application
import falcon

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
        app = application.Application.get(appid)
        if not app:
            raise falcon.HTTPInvalidParam("Application could not be found", 'appid')
        users = [a for a in app.fields.users.all()]
        resp.body = {"users": users}
        return True
