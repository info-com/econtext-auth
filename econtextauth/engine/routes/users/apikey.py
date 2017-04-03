import logging

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
