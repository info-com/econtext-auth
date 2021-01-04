import logging
from econtext.util.falcon.route import Route
import falcon
log = logging.getLogger('econtextauth')


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
        mapper = self.meta.get('mapper')
        app = mapper.application.Application.get_by_uid(appid, user_flag=True)
        if not app:
            raise falcon.HTTPInvalidParam("Application could not be found", appid)
        
        if req.get_param('minimal'):
            users = [u.to_dict_minimal() for u in app.users]
        else:
            users = [u.to_dict() for u in app.users]
        
        resp.body = {"users": users}
        return True
