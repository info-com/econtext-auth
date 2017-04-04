import logging
from econtextauth import models
from pprint import pprint
import remodel.utils
import remodel.connection
import rethinkdb as r
log = logging.getLogger('econtext')


class Apikey:
    """
    Search

    GET - Search for an apikey
    """
    routes = [
        'users/apikey',
        'users/apikey/{apikey}'

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
        #pprint(vars(new_user))
        resp.body = search_key
        return True

