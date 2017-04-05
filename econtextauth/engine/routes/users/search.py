import logging
log = logging.getLogger('econtext')
from econtextauth import models

class Search:
    """
    Search

    GET - Search for a user
    """
    routes = [
        'users/search/{search}',
    ]

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Search(*args)

    def __init__(self, econtext):
        self.econtext = econtext

    def on_get(self, req, resp, search):
        """
        Retrieve a list of users that match the provided search term

        :type search: str
        
        :param req:
        :param resp:
        :param search: A string to search for
        :return:
        """

        """
        regex? partial match? which fields to compare?
        get whole table, search fields
        
        """
        user_search=models.user.user.User.get(name=search)

        resp.body = user_search
        return True
