import logging
import falcon
from econtext.util.falcon.route import Route

from ....models.organization import Organization as EOrganization
from ....models.data import Data
from ....util import parse_datetime


class Organization(Route):
    """
    Organization
    
    An Organization is a base Node that stores a number of Users. Users
    may not exist without an Organization. An Organization may store
    custom_data (deprecated) and Data nodes that populate data for
    individuals attached to the Organization.
    
    GET  - Retrieve an Organization
    POST - Create a new Organization
    PUT  - Update an Organization
    DELETE - Remove an Organization (updates status to deleted - doesn't actually remove the record)
    """
    
    def on_get(self, req, resp, orgid):
        """
        Retrieve an Organization specified by id

        :param req:
        :param resp:
        :param orgid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.organization.Organization.get_by_uid(orgid, user_flag=True)
        if o is None:
            raise falcon.HTTPInvalidParam('Organization not found', orgid)
        resp.body = {"organization": o.to_dict()}
        return True
    
    def on_post(self, req, resp):
        """
        Create a new Organization

        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        body = req.context['body']
        o = EOrganization(
            uid=body.get('id'),
            name=body.get('name'),
            status=body.get('status', 'ENABLED'),
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
        
        o = mapper.organization.Organization.create_from_object(o)
        resp.body = {"organization": o.to_dict()}
        return True

    def on_put(self, req, resp, orgid):
        """
        Update an Organization specified by the appid

        This function should receive (key, value) pairs to update.
        Ultimately, the Organization should be retrieved, changed fields
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
        o = mapper.organization.Organization.get_by_uid(orgid)
        if o is None:
            raise falcon.HTTPInvalidParam('Organization not found', 'orgid')
        
        body = req.context['body']
        # look for changes to name, description, status, parameters, and data
        if 'name' in body:
            o.set_name(body['name'].strip())
        if 'status' in body:
            o.set_status(body['status'].strip())
        if 'custom_data' in body and isinstance(body['custom_data'], dict):
            o.set_custom_data(body['custom_data'])
        if 'data' in body and isinstance(body['data'], list):
            # body['data'] = [{'key': 'spam', 'value': 'eggs'}, ...]
            o.set_data(body['data'])
        
        o = mapper.organization.Organization.update_from_object(o)
        resp.body = {"organization": o.to_dict()}
        return True

    def on_delete(self, req, resp, orgid):
        """
        Remove an Organization specified by the orgid
        
        :param req:
        :param resp:
        :param appid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.organization.Organization.get_by_uid(orgid, user_flag=True)
        if o is None:
            raise falcon.HTTPInvalidParam('Organization not found', orgid)
        if o.status != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'Organization must be disabled before deletion is possible')
        
        if len(o.users) > 0 or len(o.admins) > 0:
            raise falcon.HTTPConflict(
                falcon.HTTP_409,
                'Users must be deleted or updated before application deletion is possible'
            )
        
        mapper.organization.Organization.delete_from_object(o)
        resp.body = {"deleted": True}
        return True
