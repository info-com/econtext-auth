import logging
import falcon
import json
from econtext.util.falcon.route import Route

from ....models.user import User as EUser
from ....models.data import Data
from ....models.organization import Organization
from ....util import parse_datetime

log = logging.getLogger('econtext')


class User(Route):
    """
    User
    
    GET  - Retrieve a User
    POST - Create a new User
    PUT  - Update a User
    DELETE - Remove a User
    """
    
    def on_get(self, req, resp, userid):
        """
        Retrieve a User specified by id

        :param req:
        :param resp:
        :param userid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.user.User.get_by_uid(userid, organization_flag=True, application_flag=True, group_flag=True, apikey_flag=True)
        if o is None:
            raise falcon.HTTPInvalidParam('User not found', userid)
        resp.body = {"user": o.to_dict()}
        return True
    
    def on_post(self, req, resp):
        """
        Create a new User

        :param req:
        :param resp:
        :return:
        """
        mapper = self.meta.get('mapper')
        body = req.context['body']
        
        # pull in related nodes
        _org_id = body.get('organization', None)
        _application_ids = set(body.get('applications', list()))
        _group_ids = set(body.get('groups', list()))
        org = mapper.organization.Organization.get_by_uid(_org_id)
        applications = mapper.application.Application.get_by_uids(_application_ids)
        groups = mapper.group.Group.get_by_uids(_group_ids)
        
        application_ids = {o.uid for o in applications}
        group_ids = {o.uid for o in groups}
        
        if _org_id is None:
            # create a new organization...
            company_name = body.get('name')
            if 'custom_data' in body and 'company_name' in body['custom_data']:
                company_name = body['custom_data']['company_name']
            org = mapper.organization.Organization.create_from_object(Organization(name=company_name))
            body['org_admin'] = True
        
        if not org:
            raise Exception(f"Organization not found: {_org_id}")
        
        if _application_ids.difference(application_ids):
            raise Exception("Some applications not found: %s" % json.dumps(_application_ids.difference(application_ids)))
        
        if _group_ids.difference(group_ids):
            raise Exception("Some groups not found: %s" % json.dumps(_group_ids.difference(group_ids)))
        
        o = EUser(
            uid=body.get('id'),
            name=body.get('name', '').strip(),
            email=body.get('email', '').strip(),
            username=body.get('username', '').strip(),
            status=body.get('status', 'ENABLED'),
            created_at=parse_datetime(body.get('created_at')),
            modified_at=parse_datetime(body.get('modified_at')),
            org_admin=body.get('org_admin', False)
        )
        o.set_password(body.get('password', '').strip())
        
        o.organization = org
        o.applications = applications
        o.groups = groups
        
        for k, v in body.get('custom_data', dict()).items():
            o.data.add(Data(
                key=k,
                value=v
            ))
        for data_item in body.get('data', list()):
            o.data.add(Data(**data_item))
        
        o = mapper.user.User.create_from_object(o)
        resp.body = {"user": o.to_dict()}
        return True

    def on_put(self, req, resp, userid):
        """
        Update a User specified by the userid

        This function should receive (key, value) pairs to update.
        Ultimately, the User should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database.
        
        `custom_data` and `data` are very similar, and if data is
        included it will over-ride custom_data, if custom_data is
        included. `custom_data` is deprecated, and will be removed in
        the future.
        
        Relationships are not directly managed/edited here, but rather
        in specific other calls.
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.user.User.get_by_uid(userid)
        if o is None:
            raise falcon.HTTPInvalidParam('User not found', userid)
        
        body = req.context['body']
        # look for changes to name, description, status, parameters, and data
        if 'name' in body:
            o.set_name(body['name'].strip())
        if 'username' in body:
            o.set_username(body['username'].strip())
        if 'email' in body:
            o.set_email(body['email'].strip())
        if 'password' in body:
            o.set_password(body['password'].strip())
        if 'status' in body:
            o.set_status(body['status'].strip())
        if 'org_admin' in body:
            o.set_org_admin(body['org_admin'])
        if 'custom_data' in body and isinstance(body['custom_data'], dict):
            o.set_custom_data(body['custom_data'])
        if 'data' in body and isinstance(body['data'], list):
            # body['data'] = [{'key': 'spam', 'value': 'eggs'}, ...]
            o.set_data(body['data'])
        
        o = mapper.user.User.update_from_object(o)
        resp.body = {"user": o.to_dict()}
        return True

    def on_delete(self, req, resp, userid):
        """
        Remove a User specified by the userid
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        mapper = self.meta.get('mapper')
        o = mapper.user.User.get_by_uid(userid)
        if o is None:
            raise falcon.HTTPInvalidParam('User not found', userid)
        if o.status != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'User must be disabled before deletion is possible')
        
        mapper.user.User.delete_from_object(o)
        resp.body = {"deleted": True}
        return True
