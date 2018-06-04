import logging
from econtextauth.models.application import application
from econtextauth.models.group import group
from econtext.util.falcon.route import Route
import falcon

log = logging.getLogger('econtext')


class Groups(Route):
    """
    Groups

    GET  - Retrieve all groups associated with a particular application
    """
    
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
