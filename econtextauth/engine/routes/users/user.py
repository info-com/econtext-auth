from econtextauth import models
import logging

log = logging.getLogger('econtext')


class User:
    """
    Users

    POST - Create a new user
    GET  - Retrieve a user
    PUT  - Update a user
    DELETE - Remove a user (updates status to deleted - doesn't actually remove the record)
    """
    routes = ['users/user', 'users/user/{userid}']
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return User(*args)
    
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
        body = req.context['body']
        application_id = body.get('applicationId')
        log.debug(application_id)
        if not application_id:
            resp.body = 'No application ID provided'
            return False
        user_application = models.application.application.Application.get(application_id)
        
        log.debug(user_application)
        
        if user_application:
            new_user = models.user.user.User.create_new(body['email'], body['password'])
            new_user["applications"].add(user_application)
            user_application["users"].add(new_user)
        else:
            resp.body = "Invalid application ID!"
            return False
        # print user_application["users"].count()
        # print list(user_application["users"].all())
        # print new_user["applications"].count()
        
        resp.body = new_user
        return True
    
    def on_get(self, req, resp, userid):
        """
        Retrieve a user specified by id
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        new_user = models.user.user.User.get(userid)
        # pprint(vars(new_user))
        resp.body = new_user
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
        
        userid = userid or None
        body = req.context['body']
        update_user = models.user.user.User.get(userid)
        
        for k in body:
            update_user[k] = body[k]
            log.debug(update_user[k], body[k])
        
        update_user.save()
        log.debug(update_user)
        resp.body = update_user
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
        
        userid = userid or None
        delete_user = models.user.user.User.get(userid)
        delete_user["status"] = "DELETED"
        delete_user.save()
        
        resp.body = delete_user
        return True
