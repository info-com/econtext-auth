import logging
from econtextauth import models

log = logging.getLogger('econtext')


class Apikey:
    """
    Search

    GET - Search for an apikey
    POST-Adds new apikey to user
    """
    routes = [
        'users/user/{userid}/apikey'
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
        
        #check next 2 lines.. Are they necessary?
        search_user["api_keys"].add(new_apikey)
        search_user.save()
        # print search_user["api_keys"].count()
        # print list(search_user["api_keys"].all())
        
        resp.body = new_apikey
        return True
