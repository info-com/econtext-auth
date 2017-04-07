import logging
from econtextauth import models

log = logging.getLogger('econtext')


class Add:
    """
    Add

    POST-Adds a groupId or applicationID to a given user
    """
    routes = ['users/user/{userid}/add']
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Add(*args)
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    def on_post(self, req, resp, userid):
        """
        
        :param req:
        :param resp:

        todo: Cleanup reused code into functions!!!
        """
        
        search_user = models.user.user.User.get(userid)
        if not search_user:
            raise Exception("No user found with userid")
        body = req.context['body']
        if (body.get('type') == 'application'):
            
            # SURROUND TRY CATCH??
            applicationId = body.get('applicationId')
            if not applicationId:
                raise Exception("Must pass an applicationId to add", applicationId)
            
            applicaiton_model = models.application.application.Application.get(applicationId)
            if not applicaiton_model:
                raise Exception("Must have a VALID applicationId: ", applicationId)
            search_user["applications"].add(applicaiton_model)
            search_user.save()
            resp.body = search_user
            return True
        
        elif (body.get('type') == 'group'):
            
            # SURROUND TRY CATCH??
            groupId = body.get('groupId')
            if not groupId:
                raise Exception("Must pass a groupId to add: ", groupId)
            group_model = models.group.group.Group.get(groupId)
            if not group_model:
                raise Exception("Must pass a VALID groupId: ", groupId)
            search_user["groups"].add(group_model)
            search_user.save()
            resp.body = search_user
            return True
        
        else:
            raise Exception("Can only add application or group!")
