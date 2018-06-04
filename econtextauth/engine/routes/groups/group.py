import logging
import remodel.utils
import remodel.connection
import falcon
from econtextauth.models.group import group
from econtext.util.falcon.route import Route

log = logging.getLogger('econtext')


class Group(Route):
    """
       Groups

       POST - Create a new group
       GET  - Retrieve a group
       PUT  - Update a group
       DELETE - Remove a group (updates status to deleted - doesn't actually remove the record)
    """
    
    def on_post(self, req, resp):
        """
        Create a new Group.
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
        grp = group.Group.create_new(
            name=body.get('name'),
            description=body.get('description'),
            status=body.get('status', 'ENABLED'),
            custom_data=body.get('custom_data'),
            id_=body.get('id'),
            app_id=body.get('application')
        )
        
        resp.body = {"group": grp}
        return True
    
    def on_get(self, req, resp, groupid):
        """
        Retrieve a group specified by id

        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        grp = group.Group.get(groupid)
        if grp is None:
            raise falcon.HTTPInvalidParam('Group not found')
        resp.body = {"group": grp}
        return True
    
    def on_put(self, req, resp, groupid):
        """
        Update a group specified by the groupid

        This function should receive (key, value) pairs to update.
        Ultimately, the group should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database

        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        body = req.context['body']
        grp = group.Group.get(groupid)
        if grp is None:
            raise falcon.HTTPInvalidParam('Group not found', 'groupid')
        grp.update_model(body)
        resp.body = {"group": grp}
        return True
    
    def on_delete(self, req, resp, groupid):
        """
        Remove a group specified by the groupid

        The group specified should have the status changed to "deleted"

        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        grp = group.Group.get(groupid)
        if not grp:
            raise falcon.HTTPInvalidParam('Group not found', 'groupid')
        if grp.get('status') != 'DISABLED':
            raise falcon.HTTPConflict(falcon.HTTP_409, 'Group must be disabled before deletion is possible')
        grp.delete()
        resp.body = {"deleted": True}
        return True
