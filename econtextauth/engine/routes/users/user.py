from econtextauth import models
import logging
import falcon
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class User(Route):
    """
    Users

    POST - Create a new user
    GET  - Retrieve a user
    PUT  - Update a user
    DELETE - Remove a user (updates status to deleted - doesn't actually remove the record)
    """
    
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
        body = req.context['body']
        try:
            user = models.user.user.User.create_new(
                email=body['email'],
                password=body['password'],
                applications=body['applications'],
                name=body.get('name'),
                custom_data=body.get('custom_data'),
                status=body.get('status', 'UNVERIFIED'),
                id_=body.get('id'),
                username=body.get('username', body['email']),
                groups=body.get('groups')
            )
        except KeyError as e:
            raise falcon.HTTPMissingParam(e.message)
        except Exception as e:
            raise e
        
        resp.body = {"user": user}
        return True
    
    def on_get(self, req, resp, userid):
        """
        Retrieve a user specified by id
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        user = models.user.user.User.get(userid)
        if user is None:
            raise falcon.HTTPInvalidParam('User not found', 'userid')
        resp.body = {"user": user}
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
        body = req.context['body']
        user = models.user.user.User.get(userid)
        if user is None:
            raise falcon.HTTPInvalidParam('User not found', 'userid')
        
        user.update_model(body)
        resp.body = {"user": user}
        return True
    
    def on_delete(self, req, resp, userid):
        """
        Remove a user specified by the userid
        
        The user specified should have the status changed to "deleted"
        
        This function will also remove all associated API keys from the user.
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        user = models.user.user.User.get(userid)
        if not user:
            raise falcon.HTTPInvalidParam('User not found', 'userid')
        if user.get('status') != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'User must be disabled before deletion is possible')
        
        for api_key in user.fields.api_keys.all():
            api_key.delete()
        
        user.delete()
        resp.body = {"deleted": True}
        return True
