import logging
from econtextauth import models
log = logging.getLogger('econtext')


class Apikey:
    """
    Search

    GET - Search for an apikey
    """
    routes = [
        'users/user/{userid}/apikey'
    ]

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Apikey(*args)

    def __init__(self, econtext):
        self.econtext = econtext

    def on_get(self, req, resp, apikey):
        """
        Retrieve an apikey
        :type apikey: str

        :param req:
        :param resp:
        :param apikey: A string to search for apikey
        :return:
        """

        search_key = models.user.apikey.ApiKey.get(apikey)
        resp.body = search_key
        return True



    def on_post(self,req,resp,userid):
        """
        Create an APIKEY
        :param req:
        :param resp:
        
        """

        search_user=models.user.user.User.get(userid)
        body = req.context['body']
        new_apikey=models.user.apikey.ApiKey.create_new(body.get('name'),body.get('description'))
        search_user["api_keys"].add(new_apikey)
        #print search_user["api_keys"].count()
        #print list(search_user["api_keys"].all())

        resp.body=new_apikey
        return True