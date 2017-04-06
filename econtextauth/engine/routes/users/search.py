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
        
        user_search = models.user.user.User.objects.query.filter(lambda user: (user['email'].match(search)) | (user['name'].match(search)) | (user['id'].match(search))).run()
        log.debug(type(user_search))

        apikey_search=models.user.apikey.ApiKey.objects.query.filter(lambda apikey: (apikey['id'].match(search))).run()
        log.debug(apikey_search)
        log.debug(user_search)
        resp.body = user_search
        return True
