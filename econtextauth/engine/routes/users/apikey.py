import logging
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
            raise Exception('User not found')
        
        key = models.user.apikey.ApiKey.create_new(
            user=user,
            name=body.get('name'),
            description=body.get('description'),
            id_=body.get('id'),
            secret=body.get('secret')
        )
        resp.body = key
        return True

    def on_put(self, req, resp, userid, apikeyid):
        key = models.user.apikey.ApiKey.get(apikeyid)
        if not key:
            raise Exception('ApiKey not found')
        
        body = req.context['body']
        
        mod_apikey = models.user.apikey.ApiKey.edit_apikey(key, **body)
        resp.body = mod_apikey
        resp.body = key
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
        key = models.user.apikey.ApiKey.get(apikeyid)
        if not key:
            raise Exception('ApiKey not found')
        key['status'] = 'DELETED'
        key.save()
    
        resp.body = key
        return True
