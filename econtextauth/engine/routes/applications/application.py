import logging
import remodel.utils
import remodel.connection
from econtextauth import models

log = logging.getLogger('econtext')


class Application:
    """
       Application

       POST - Create a new Application
       GET  - Retrieve an Application
       PUT  - Update an application
       DELETE - Remove an applciation (updates status to deleted - doesn't actually remove the record)
       """
    routes = ['applications/application', 'applications/application/{applicationid}']
    
    remodel.connection.pool.configure(db="econtext_users")
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Application(*args)
    
    def __init__(self, econtext):
        self.econtext = econtext
    
    def on_post(self, req, resp):
        """
        Create a new Application.
            id
            name
            description
            status
            createdAt
            modifiedAt
            customData

        :todo

        :param req:
        :param resp:
        :return:
        """
        body = req.context['body']
        new_application = models.application.application.Application.create_new(name=body.get('name'),
                                                                                description=body.get('description'))
        resp.body = new_application
        return True
    
    def on_get(self, req, resp, applicationid):
        """
        Retrieve an application specified by id

        :param req:
        :param resp:
        :param applicationid:
        :return:
        """
        new_application = models.application.application.Application.get(applicationid)
        resp.body = new_application
        return True
    
    def on_put(self, req, resp, applicationid):
        """
        Update an application specified by the applicaitonid

        This function should receive (key, value) pairs to update.
        Ultimately, the application should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database

        :param req:
        :param resp:
        :param applicationid:
        :return:
        """
        
        applicationId = applicationid or None
        body = req.context['body']
        update_application = models.application.application.Application.get(applicationId)
        for k in body:
            update_application[k] = body[k]
            log.debug(update_application[k], body[k])
        
        update_application.save()
        log.debug(update_application)
        resp.body = update_application
        return True
    
    def on_delete(self, req, resp, applicationid):
        """
        Remove an application specified by the applicationId

        The application specified should have the status changed to "deleted"

        :param req:
        :param resp:
        :param applicationId:
        :return:
        """
        applicationId = applicationid or None
        delete_application = models.application.application.Application.get(applicationId)
        delete_application["status"] = "DELETED"
        delete_application.save()
        
        resp.body = delete_application
        return True
