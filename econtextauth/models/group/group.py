"""
Group Object

Should contain the following fields:

id
name
description
status
createdAt
modifiedAt
customData
"""
from remodel.models import Model, before_save
from rethinkdb import now
from econtextauth import get_base_url
from econtextauth.models.application import application
import logging
import falcon
log = logging.getLogger('econtext')


class Group(Model):
    has_many = ("User",)
    belongs_to = ("Application", )

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            'id': self.fields.id,
            'name': self.get('name'),
            'description': self.get('description'),
            'status': self.get('status'),
            'custom_data': self.get('custom_data'),
            'created_at': str(self.get('created_at', '')),
            'modified_at': str(self.get('modified_at', '')),
            'application': self['application']['id'],
            'href': '{}/api/groups/group/{}'.format(get_base_url(), self.fields.id)
        }
    
    @staticmethod
    def create_new(name, description=None, status='ENABLED', custom_data=None, app_id=None, id_=None, *args, **kwargs):
        """
        Create a new Group object
        """
        if not name:
            raise falcon.HTTPMissingParam('name')
        if not app_id:
            raise falcon.HTTPMissingParam('application')
        
        created_at = now()
        app = Group.check_application(app_id)
        
        grp = Group(
            name=name.strip(),
            description=description,
            custom_data=custom_data,
            status=status,
            created_at=created_at
        )
        if id_ and id_.strip() != '':
            if Group.id_already_exists(id_):
                raise falcon.HTTPInvalidParam("A Group with that id already exists")
            grp['id'] = id_
        
        if grp.already_exists(name.strip(), app):
            raise falcon.HTTPInvalidParam("A Group with that name already exists")
        
        grp.save()
        # Add in connected applications
        grp['application'] = app
        grp.save()
        return grp
    
    def validate_custom_data(self, custom_data=None):
        if not custom_data or not isinstance(custom_data, (dict,)):
            return None
        return custom_data

    def update_model(self, updates=None):
        """
        Updates a Group

        :return:
        """
        if updates is None:
            return
        
        if 'name' in updates:
            if self.already_exists(updates.get('name').strip()):
                raise falcon.HTTPInvalidParam("A Group with that name already exists")
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
    
    @staticmethod
    def check_application(app_id):
        app = application.Application.get(app_id)
        if not app:
            raise falcon.HTTPInvalidParam("Couldn't find application {}".format(app_id))
        return app
    
    @before_save
    def update_modification_time(self):
        """
        Update the modified_at parameter whenever we save

        :return:
        """
        self.fields.modified_at = now()
        return True
    
    @staticmethod
    def id_already_exists(id_):
        """
        Check to see if a record already exists with this id
        :param id_:
        :return:
        """
        if Group.get(id_):
            return True
        return False
    
    def already_exists(self, group_name, app=None):
        """
        Check to see whether another group already exists in the same
        application with the same name
        
        :param group_name:
        :return boolean:
        """
        if not app:
            app = self['application']
        for grp in Group.filter(name=group_name.strip()):
            if grp['id'] == self.get('id'):
                continue
            if grp['application']['id'] == app['id']:
                return True
        return False
