import logging
from econtext.util.falcon.route import Route
import falcon
log = logging.getLogger('econtextauth')


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
        mapper = self.meta.get('mapper')
        app = mapper.application.Application.get_by_uid(appid, group_flag=True)
        if not app:
            raise falcon.HTTPInvalidParam("Application could not be found", appid)

        groups = [g.to_dict() for g in app.groups]
        resp.body = {"groups": groups}
        return True
