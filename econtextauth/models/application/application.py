"""
Application Object

Should contain the following fields:

id
name
description
status
createdAt
modifiedAt
customData
"""
from econtextauth import get_base_url
from remodel.models import Model, before_save
from rethinkdb import now
import logging
import falcon
log = logging.getLogger('econtext')


class Application(Model):
    has_and_belongs_to_many = ("User", "Group")
    
    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            'id': self.fields.id,
            'name': self.get('name'),
            'description': self.get('description'),
            'custom_data': self.get('custom_data'),
            'status': self.get('status'),
            'created_at': str(self.get('created_at') or ''),
            'modified_at': str(self.get('modified_at') or ''),
            'href': '{}/api/applications/application/{}'.format(get_base_url(), self.fields.id)
        }
    
    @staticmethod
    def create_new(name, description=None, status='ENABLED', custom_data=None, id_=None, *args, **kwargs):
        """
        Create a new Application object
        """
        if not name:
            raise falcon.HTTPMissingParam("An Application must have a name", 'name')
        if Application.already_exists(name.strip()):
            raise falcon.HTTPInvalidParam("An application with that name already exists", 'name')
        
        created_at = now()
        
        app = Application(
            name=name.strip(),
            description=description,
            custom_data=custom_data,
            status=status,
            created_at=created_at
        )
        
        if id_ and id_.strip() != '':
            if Application.id_already_exists(id_):
                raise falcon.HTTPInvalidParam("An Application with that id already exists", 'id')
            app['id'] = id_
        
        app.save()
        return app
    
    def validate_custom_data(self, custom_data=None):
        if not custom_data or not isinstance(custom_data, (dict,)):
            return dict()
        return custom_data

    def update_model(self, updates=None):
        """
        Updates an Application

        :return:
        """
        if updates is None:
            return
        
        if 'name' in updates:
            if Application.already_exists(updates.get('name').strip()):
                raise falcon.HTTPInvalidParam("An application with that name already exists", 'name')
            updates['name'] = updates['name'].strip()
        
        if 'custom_data' in updates:
            custom_data = updates.pop('custom_data')
            self['custom_data'] = self.validate_custom_data(custom_data)
        
        updates.pop('created_at', None)
        for k, v in updates.items():
            if k in ('name', 'description', 'status'):
                self[k] = v
        
        self.save()
        return self
    
    @before_save
    def update_modification_time(self):
        """
        Update the modified_at parameter whenever we save
        
        :return:
        """
        self['modified_at'] = now()
        return True
    
    @staticmethod
    def id_already_exists(id_):
        """
        Check to see if a record already exists with this id
        :param id:
        :return:
        """
        if Application.get(id_):
            return True
        return False
    
    @staticmethod
    def already_exists(name):
        """
        Check to see if a record exists already with this application name
        
        :param name:
        :return boolean:
        """
        if Application.get(name=name):
            return True
        return False
