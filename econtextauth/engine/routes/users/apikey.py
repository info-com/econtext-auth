import logging
import falcon
from econtextauth import models

log = logging.getLogger('econtext')


class Apikey:
    """
    Search

    POST - Adds new apikey to user
    PUT - updates name, desc, or status
    DELETE - REMOVES an APIKEY!
    """
    routes = [
        'users/user/{userid}/apikey',
        'users/user/{userid}/apikey/{apikeyid}'
    ]

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Apikey(*args)

    def __init__(self, econtext):
        self.econtext = econtext
    
    def on_get(self, req, resp, userid, apikeyid):
        """
        GET an ApiKey object
        
        :param req:
        :param resp:
        :param userid:
        :param apikeyid:
        :return:
        """
        user = models.user.user.User.get(userid)
        key = models.user.apikey.ApiKey.get(apikeyid)
        if user is None:
            raise falcon.HTTPInvalidParam('User not found')
        if not key:
            raise falcon.HTTPInvalidParam('ApiKey not found')
        resp.body = {"apikey": key}
        return True
    
    def on_post(self, req, resp, userid):
        """
        Create a new ApiKey and attach it to a user
        
        :param req:
        :param resp:
        :param userid:
        """
        body = req.context['body']
        user = models.user.user.User.get(userid)
        if not user:
            raise falcon.HTTPInvalidParam('User not found')
        
        key = models.user.apikey.ApiKey.create_new(
            user=user,
            name=body.get('name'),
            description=body.get('description'),
            id_=body.get('id'),
            secret=body.get('secret')
        )
        resp_dict = key.json
        resp_dict['secret'] = key.fields.secret
        resp.body = {"apikey": resp_dict}
        return True

    def on_put(self, req, resp, userid, apikeyid):
        user = models.user.user.User.get(userid)
        key = models.user.apikey.ApiKey.get(apikeyid)
        if user is None:
            raise falcon.HTTPInvalidParam('User not found')
        if not key:
            raise falcon.HTTPInvalidParam('ApiKey not found')
        body = req.context['body']
        key.update_model(body)
        resp.body = {"apikey": key}
        return True

    def on_delete(self, req, resp, userid, apikeyid):
        """
        Remove a user specified by the userid

        The user specified should have the status changed to "deleted"

        :param req:
        :param resp:
        :param userid:
        :return:
        """
        user = models.user.user.User.get(userid)
        key = models.user.apikey.ApiKey.get(apikeyid)
        if user is None:
            raise falcon.HTTPInvalidParam('User not found')
        if not key:
            raise falcon.HTTPInvalidParam('ApiKey not found')
        if key.get('status') != 'DISABLED':
            raise falcon.HTTPConflict('ApiKey must be disabled before deletion is possible')
        
        key.delete()
        resp.body = {"deleted": True}
        return True
