import logging
from econtextauth import models

log = logging.getLogger('econtext')


class Apikey:
    """
    Search

    PUT - updates name, desc, or status
    POST-Adds new apikey to user
    DELETE-REMOVES an APIKEY!
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
        Create an APIKEY
        :param req:
        :param resp:
        
        """

        search_user = models.user.user.User.get(userid)
        if not search_user:
            raise Exception('No user found with apikey')
        body = req.context['body']
        new_apikey = models.user.apikey.ApiKey.create_new(body.get('name'), body.get('description'))
        
        search_user["api_keys"].add(new_apikey)
        search_user.save()
        # print search_user["api_keys"].count()
        # print list(search_user["api_keys"].all())
        
        resp.body = new_apikey
        return True


    def on_put(self,req,resp,userid,apikeyid):
        update_apikey = models.user.apikey.ApiKey.get(apikeyid)
        if not update_apikey:
            raise Exception('No apikey found')
        
        body = req.context['body']
        mod_apikey=models.user.apikey.ApiKey.edit_apikey(update_apikey,**body)
        resp.body=mod_apikey
        resp.body=update_apikey
        return True

    def on_delete(self, req, resp, userid):
        """
        Remove a user specified by the userid

        The user specified should have the status changed to "deleted"

        :param req:
        :param resp:
        :param userid:
        :return:
        """
    
        userid = userid or None
        delete_user = models.user.user.User.get(userid)
        delete_user["status"] = "DISABLED"
        delete_user.save()
    
        resp.body = delete_user
        return True
