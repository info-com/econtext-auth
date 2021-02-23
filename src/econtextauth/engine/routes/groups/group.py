import logging
import falcon
from econtext.util.falcon.route import Route

from ....models.group import Group as EGroup
from ....models.data import Data
from ....util import parse_datetime


class Group(Route):
    """
    Group
    
    A Group is a collection of User objects
    
    GET  - Retrieve a Group
    POST - Create a new Group
    PUT  - Update a Group
    DELETE - Remove a Group
    """
    
    def on_get(self, req, resp, groupid):
        """
        Retrieve a Group specified by id

        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.group.Group.get_by_uid(groupid)
        if o is None:
            raise falcon.HTTPInvalidParam('Organization not found', groupid)
        resp.body = {"group": o.to_dict()}
        return True
    
    def on_post(self, req, resp):
        """
        Create a new Group

        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        body = req.context['body']
        o = EGroup(
            uid=body.get('id'),
            name=body.get('name'),
            description=body.get('description'),
            status=body.get('status', 'ENABLED'),
            application=body.get('application'),
            created_at=parse_datetime(body.get('created_at')),
            modified_at=parse_datetime(body.get('modified_at'))
        )
        
        for k, v in body.get('custom_data', dict()).items():
            if k in ('', '_empty_'):
                continue
            o.data.add(Data(
                key=k,
                value=v
            ))
        for data_item in body.get('data', list()):
            o.data.add(Data(**data_item))
        
        o = mapper.group.Group.create_from_object(o)
        resp.body = {"group": o.to_dict()}
        return True

    def on_put(self, req, resp, groupid):
        """
        Update a Group specified by the groupid

        This function should receive (key, value) pairs to update.
        Ultimately, the Group should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database.
        
        `custom_data` and `data` are very similar, and if data is
        included it will over-ride custom_data, if custom_data is
        included. `custom_data` is deprecated, and will be removed in
        the future.
        
        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.group.Group.get_by_uid(groupid)
        if o is None:
            raise falcon.HTTPInvalidParam('Group not found', groupid)
        
        body = req.context['body']
        # look for changes to name, description, status, parameters, and data
        if 'name' in body:
            o.set_name(body['name'].strip())
        if 'description' in body:
            o.set_description(body['description'].strip())
        if 'status' in body:
            o.set_status(body['status'].strip())
        if 'custom_data' in body and isinstance(body['custom_data'], dict):
            o.set_custom_data(body['custom_data'])
        if 'data' in body and isinstance(body['data'], list):
            # body['data'] = [{'key': 'spam', 'value': 'eggs'}, ...]
            o.set_data(body['data'])
        
        o = mapper.group.Group.update_from_object(o)
        resp.body = {"group": o.to_dict()}
        return True

    def on_delete(self, req, resp, groupid):
        """
        Remove a Group specified by the groupid
        
        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.group.Group.get_by_uid(groupid, user_flag=True)
        if o is None:
            raise falcon.HTTPInvalidParam('Group not found', groupid)
        if o.status != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'Group must be disabled before deletion is possible')
        
        if len(o.users) > 0:
            raise falcon.HTTPConflict(
                falcon.HTTP_409,
                'Users must be deleted or updated before group deletion is possible'
            )
        
        mapper.group.Group.delete_from_object(o)
        resp.body = {"deleted": True}
        return True
