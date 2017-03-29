import logging
log = logging.getLogger('econtext')


class Users:
    """
    Users

    POST - Create a new user
    GET  - Retrieve a user
    PUT  - Update a user
    DELETE - Remove a user (updates status to deleted - doesn't actually remove the record)
    """
    routes = [
        'users',
        'users/{userid}'
    ]
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Users(*args)
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    def on_post(self, req, resp):
        """
        Create a new User.
        
        Requires, at minimum, a username(email), and password.  In
        order to actually be used to login anywhere, we also need
        membership in an application.
        
        A globally unique id should also be generated for each new user
        and is used as the primary key in the database.  Existing ids
        formats may be different from these.
        
        :todo work out the id structure
        
        :param req:
        :param resp:
        :return:
        """
        resp.body = "ok"
        return True
    
    def on_get(self, req, resp, userid):
        """
        Retrieve a user specified by id
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        resp.body = "ok"
        return True
    
    def on_put(self, req, resp, userid):
        """
        Update a user specified by the userid
        
        This function should receive (key, value) pairs to update.
        Ultimately, the user should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        resp.body = "ok"
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
        resp.body = "ok"
        return True