import logging
import remodel.utils
import remodel.connection
import falcon
from econtext.util.falcon.route import Route
from econtext.util.log import log
from econtextauth.models.application import application


class Application(Route):
    """
    Application
    
    POST - Create a new Application
    GET  - Retrieve an Application
    PUT  - Update an application
    DELETE - Remove an applciation (updates status to deleted - doesn't actually remove the record)
    """
    
    def on_post(self, req, resp):
        """
        Create a new Application

        :param req:
        :param resp:
        :return:
        """
        body = req.context['body']
        app = application.Application.create_new(
            name=body.get('name'),
            description=body.get('description'),
            status=body.get('status', 'ENABLED'),
            custom_data=body.get('custom_data'),
            jwt_secret=body.get('jwt_secret'),
            id_=body.get('id')
        )
        resp.body = {"application": app}
        return True
    
    def on_get(self, req, resp, appid):
        """
        Retrieve an application specified by id

        :param req:
        :param resp:
        :param appid:
        :return:
        """
        app = application.Application.get(appid)
        if app is None:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        resp.body = {"application": app}
        return True

    def on_put(self, req, resp, appid):
        """
        Update an application specified by the appid

        This function should receive (key, value) pairs to update.
        Ultimately, the application should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database

        :param req:
        :param resp:
        :param appid:
        :return:
        """
        body = req.context['body']
        app = application.Application.get(appid)
        if app is None:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        app.update_model(body)
        resp.body = {"application": app}
        return True

    def on_delete(self, req, resp, appid):
        """
        Remove an application specified by the appid
        
        @todo May not delete the main app (eContext Auth)
        
        :param req:
        :param resp:
        :param appid:
        :return:
        """
        if appid == self.meta.get('application_id'):
            raise falcon.HTTPInvalidParam("Cannot delete the system application", 'appid')
        app = application.Application.get(appid)
        if app is None:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        if app.get('status') != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'Application must be disabled before deletion is possible')
        
        if app.fields.groups.count() > 0:
            raise falcon.HTTPConflict(
                falcon.HTTP_409,
                'Groups must be deleted before application deletion is possible'
            )
        
        if app.fields.users.count() > 0:
            raise falcon.HTTPConflict(
                falcon.HTTP_409,
                'Users must be deleted or updated before application deletion is possible'
            )
        
        del app['users']
        del app['groups']
        app.delete()
        resp.body = {"deleted": True}
        return True
