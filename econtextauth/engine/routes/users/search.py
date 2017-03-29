import logging
log = logging.getLogger('econtext')


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
        resp.body = "ok"
        return True
