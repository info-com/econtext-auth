import logging
from econtextauth.models.application import application
from econtextauth.models.group import group
import falcon

log = logging.getLogger('econtext')


class Groups:
    """
    Groups

    GET  - Retrieve all groups associated with a particular application
    """
    routes = ['applications/application/{appid}/groups']
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Groups(*args)
    
    def on_get(self, req, resp, appid):
        """
        Retrieve all groups belonging to an application

        :param req:
        :param resp:
        :return:
        """
        app = application.Application.get(appid)
        if not app:
            raise falcon.HTTPInvalidParam("Application could not be found", 'appid')
        groups = list(group.Group.filter(application_id=appid))
        resp.body = {"groups": groups}
        return True
