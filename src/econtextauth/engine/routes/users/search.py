import logging
import falcon
from econtext.util.falcon.route import Route
import neomodel
neomodel.util.logger.setLevel(logging.DEBUG)


class Search(Route):
    """
    Search
    
    GET - Search for a user
    """
    
    def on_get(self, req, resp, search):
        """
        Retrieve a list of users that match the provided search term

        :type search: str
        :param req:
        :param resp:
        :param search: A string to search for
        :return:
        """
        
        # Grab users based on email, name, or id
        mapper = self.meta.get('mapper')
        users = mapper.user.User.search(search, organization_flag=True, application_flag=True, group_flag=True, apikey_flag=False)
        resp.body = {"users": [u.to_dict() for u in users]}
        return True
