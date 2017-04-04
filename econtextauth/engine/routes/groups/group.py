import logging
log = logging.getLogger('econtext')
from pprint import pprint
import remodel.utils
import remodel.connection
import rethinkdb as r
from econtextauth import models


class Group:
    """
       Groups

       POST - Create a new group
       GET  - Retrieve a group
       PUT  - Update a group
       DELETE - Remove a group (updates status to deleted - doesn't actually remove the record)
       """
    routes = [
        'groups/group',
        'groups/group/{groupid}'
    ]

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
        new_group = models.group.group.Group(name=body['name'], description=body['description'])
        new_group.save()
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
        new_user = models.group.group.Group.get(groupid)
        resp.body = new_user
        return True