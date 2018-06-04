import logging
from econtextauth.models.application import application
from econtext.util.falcon.route import Route
import falcon

log = logging.getLogger('econtext')


class Users(Route):
    """
    Users

    GET  - Retrieve all users associated with a particular application
    """
    
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
        if req.get_param('minimal'):
            users = [u.json_minimal for u in users]
        resp.body = {"users": users}
        return True
