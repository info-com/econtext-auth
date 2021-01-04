import logging
import falcon
from econtext.util.falcon.route import Route
from ....models.apikey import ApiKey as EApiKey
log = logging.getLogger('econtext')


class ApiKey(Route):
    """
    ApiKey

    GET  - Retrieve an ApiKey
    POST - Create a new ApiKey
    PUT  - Update an ApiKey
    DELETE - Remove a ApiKey
    """

    def on_get(self, req, resp, userid, apikeyid):
        """
        GET an ApiKey object - read

        :param req:
        :param resp:
        :param userid:
        :param apikeyid:
        :return:
        """
        mapper = self.meta.get('mapper')
        u = mapper.user.User.get_by_uid(userid)
        o = mapper.apikey.ApiKey.get_by_key(apikeyid)
        
        if not u:
            raise Exception('User %s not found' % userid)
        if not o:
            raise Exception('ApiKey %s not found' % apikeyid)
        
        if o.user.uid != u.uid:
            raise Exception("ApiKey %s not found" % apikeyid)
        
        resp.body = {"apikey": o.to_dict_minimal()}
        return True
    
    def on_post(self, req, resp, userid):
        """
        POST a new ApiKey and attach it to a User - create
        
        :param req:
        :param resp:
        :param userid:
        """
        mapper = self.meta.get('mapper')
        body = req.context['body']
        u = mapper.user.User.get_by_uid(userid)
        if not u:
            raise Exception('User %s not found' % userid)

        o = EApiKey(
            key=body.get('key'),            # usually empty
            secret=body.get('secret'),      # usually empty
            name=body.get('name'),
            description=body.get('description'),
            status=body.get('status', 'ENABLED'),
            created_at=body.get('created_at'),
            modified_at=body.get('modified_at')
        )
        o.user = u

        o = mapper.apikey.ApiKey.create_from_object(o)
        resp.body = {"apikey": o.to_dict()}
        return True
    
    def on_put(self, req, resp, userid, apikeyid):
        """
        PUT an ApiKey object - update

        :param req:
        :param resp:
        :param userid:
        :param apikeyid:
        :return:
        """
        mapper = self.meta.get('mapper')
        u = mapper.user.User.get_by_uid(userid)
        o = mapper.apikey.ApiKey.get_by_key(apikeyid)
        
        if not u:
            raise Exception('User %s not found' % userid)
        if not o:
            raise Exception('ApiKey %s not found' % apikeyid)
        
        if o.user.uid != u.uid:
            raise Exception("ApiKey %s not found" % apikeyid)
        
        body = req.context['body']
        # look for changes to name, description, status, parameters, and data
        if 'name' in body:
            o.set_name(body['name'].strip())
        if 'description' in body:
            o.set_description(body['description'].strip())
        if 'status' in body:
            o.set_status(body['status'].strip())
        
        o = mapper.apikey.ApiKey.update_from_object(o)
        resp.body = {"apikey": o.to_dict_minimal()}
        return True

    def on_delete(self, req, resp, userid, apikeyid):
        """
        DELETE an ApiKey from a User and delete it - delete

        :param req:
        :param resp:
        :param userid:
        :return:
        """
        mapper = self.meta.get('mapper')
        u = mapper.user.User.get_by_uid(userid)
        o = mapper.apikey.ApiKey.get_by_key(apikeyid)
        
        if not u:
            raise Exception('User %s not found' % userid)
        if not o:
            raise Exception('ApiKey %s not found' % apikeyid)
        
        if o.user.uid != u.uid:
            raise Exception("ApiKey %s not found" % apikeyid)
        
        if o.status != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'ApiKey must be disabled before deletion is possible')
        
        mapper.apikey.ApiKey.delete_from_object(o)
        resp.body = {"deleted": True}
        return True
