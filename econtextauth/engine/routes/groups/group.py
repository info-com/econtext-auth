import logging
import remodel.utils
import remodel.connection
from econtextauth import models

log = logging.getLogger('econtext')


class Group:
    """
       Groups

       POST - Create a new group
       GET  - Retrieve a group
       PUT  - Update a group
       DELETE - Remove a group (updates status to deleted - doesn't actually remove the record)
    """
    routes = ['groups/group', 'groups/group/{groupid}']
    
    remodel.connection.pool.configure(db="econtext_users")
    
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Group(*args)
    
    def __init__(self, econtext):
        self.econtext = econtext
    
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
        # if body.get('name') and body.get('name') != '':
        #     name = body.get('name')
        # else:
        #     raise Exception('Name must not be empty!')
        
        new_group = models.group.group.Group.create_new(body.get('name'), description=body.get('description'))
        
        resp.body = new_group
        return True
    
    def on_get(self, req, resp, groupid):
        """
        Retrieve a group specified by id

        :param req:
        :param resp:
        :param groupid:
        :return:
        """
        get_group = models.group.group.Group.get(groupid)
        resp.body = get_group
        return True
    
    # def on_put(self, req, resp, groupid):
    #     """
    #     Update a group specified by the groupid
    #
    #     This function should receive (key, value) pairs to update.
    #     Ultimately, the group should be retrieved, changed fields
    #     verified, and then those changed fields should be updated in
    #     the database
    #
    #     :param req:
    #     :param resp:
    #     :param groupid:
    #     :return:
    #     """
    #     groupId = groupid or None
    #     body = req.context['body']
    #     update_group = models.group.group.Group.get(groupId)
    #     for k in body:
    #         update_group[k] = body[k]
    #         log.debug(update_group[k], body[k])
    #
    #     update_group.save()
    #     log.debug(update_group)
    #     resp.body = update_group
    #     return True
    #


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
        groupId = groupid or None
        body = req.context['body']
        update_group = models.group.group.Group.get(groupId)
        if update_group is None:
            raise Exception('GroupId not found!')

        update_group.save_group(update_group, **body)
        log.debug(update_group)
        resp.body = update_group
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
        groupId = groupid or None
        delete_group = models.group.group.Group.get(groupId)
        delete_group['status'] = 'DELETED'
        delete_group.save()
        
        resp.body = delete_group
        return True
