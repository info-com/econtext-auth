from econtextauth.models.user import user
import logging
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Users(Route):
    """
        Users
    
        GET  - Retrieve all users
    """
    
    def on_get(self, req, resp):
        """
            Retrieve all users
    
            :param req:
            :param resp:
            :param userid:
            :return:
        """
        users = list(user.User.all())
        if req.get_param('minimal'):
            users = [u.json_minimal for u in users]
        resp.body = {"users": users}
        return True
