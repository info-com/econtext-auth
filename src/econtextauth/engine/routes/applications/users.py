import logging
from econtext.util.falcon.route import Route
import falcon
from collections import defaultdict
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
        
        # app.users is a list of econtextauth.models.user objects (with a _object defined)
        userids = [u.uid for u in app.users]
        apikeys = mapper.apikey.ApiKey.get_apikeys_by_userids(userids)
        apikeys_by_userid = defaultdict(list)
        for uid, apikey in apikeys:
            apikeys_by_userid[uid].append(apikey)
        
        organizations = mapper.organization.Organization.get_organizations_by_userids(userids)
        # add the orgs to the users...
        user_organizations = dict()
        for uid, org in organizations:
            user_organizations[uid] = org
        for u in app.users:
            u.organization = user_organizations[u.uid]
        
        if req.get_param('minimal'):
            users = [u.to_dict_minimal() for u in app.users]
        else:
            users = list()
            for u in app.users:
                u.set_apikeys(apikeys_by_userid.get(u.uid))
                users.append(u.to_dict())
        
        resp.body = {"users": sorted(users, key=lambda x: x['username'])}
        return True
