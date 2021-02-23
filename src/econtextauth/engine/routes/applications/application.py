import logging
import falcon
from econtext.util.falcon.route import Route

from ....models.application import Application as EApplication
from ....models.application_parameter import ApplicationParameter
from ....models.data import Data
from ....util import parse_datetime


class Application(Route):
    """
    Application
    
    GET  - Retrieve an Application
    POST - Create a new Application
    PUT  - Update an application
    DELETE - Remove an applciation (updates status to deleted - doesn't actually remove the record)
    """
    
    def on_get(self, req, resp, appid):
        """
        Retrieve an application specified by id

        :param req:
        :param resp:
        :param appid:
        :return:
        """
        mapper = self.meta.get('mapper')
        app = mapper.application.Application.get_by_uid(appid)
        if app is None:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        resp.body = {"application": app.to_dict()}
        return True
    
    def on_post(self, req, resp):
        """
        Create a new Application

        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        body = req.context['body']
        app = EApplication(
            uid=body.get('id'),
            name=body.get('name'),
            description=body.get('description'),
            status=body.get('status', 'ENABLED'),
            jwt_secret=body.get('jwt_secret'),
            created_at=parse_datetime(body.get('created_at')),
            modified_at=parse_datetime(body.get('modified_at'))
        )
        for k, v in body.get('custom_data', dict()).items():
            if k in ('', '_empty_'):
                continue
            app.data.add(Data(
                key=k,
                value=v
            ))
        for data_item in body.get('data', list()):
            app.data.add(Data(**data_item))
            
        for parameter in body.get('parameters', list()):
            app.parameters.add(ApplicationParameter(**parameter))
        
        app = mapper.application.Application.create_from_object(app)
        resp.body = {"application": app.to_dict()}
        return True

    def on_put(self, req, resp, appid):
        """
        Update an application specified by the appid

        This function should receive (key, value) pairs to update.
        Ultimately, the application should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database.
        
        `custom_data` and `data` are very similar, and if data is
        included it will over-ride custom_data, if custom_data is
        included. `custom_data` is deprecated, and will be removed in
        the future.
        
        :param req:
        :param resp:
        :param appid:
        :return:
        """
        mapper = self.meta.get('mapper')
        app = mapper.application.Application.get_by_uid(appid)
        if app is None:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        
        body = req.context['body']
        # look for changes to name, description, status, parameters, and data
        if 'name' in body:
            app.set_name(body['name'].strip())
        if 'description' in body:
            app.set_description(body['description'].strip())
        if 'status' in body:
            app.set_status(body['status'].strip())
        if 'jwt_secret' in body:
            app.set_jwt_secret(body['jwt_secret'].strip())
        if 'custom_data' in body and isinstance(body['custom_data'], dict):
            app.set_custom_data(body['custom_data'])
        if 'data' in body and isinstance(body['data'], list):
            # body['data'] = [{'key': 'spam', 'value': 'eggs'}, ...]
            app.set_data(body['data'])
        if 'parameters' in body and isinstance(body['parameters'], list):
            # body['parameters'] = [{'key': 'spam', 'datatype': 'and', 'default': 'eggs', 'description': 'spam and eggs'}, ...]
            app.set_paramameters(body['params'])
        
        app = mapper.application.Application.update_from_object(app)
        resp.body = {"application": app.to_dict()}
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
        mapper = self.meta.get('mapper')
        app = mapper.application.Application.get_by_uid(appid, group_flag=True, user_flag=True)
        if app is None:
            raise falcon.HTTPInvalidParam('Application not found', 'appid')
        if app.status != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'Application must be disabled before deletion is possible')
        
        if len(app.groups) > 0:
            raise falcon.HTTPConflict(
                falcon.HTTP_409,
                'Groups must be deleted before application deletion is possible'
            )
        
        if len(app.users) > 0:
            raise falcon.HTTPConflict(
                falcon.HTTP_409,
                'Users must be deleted or updated before application deletion is possible'
            )
        
        mapper.application.Application.delete_from_object(app)
        resp.body = {"deleted": True}
        return True
