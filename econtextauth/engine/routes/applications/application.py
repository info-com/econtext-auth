import logging

log = logging.getLogger('econtext')
from pprint import pprint
import remodel.utils
import remodel.connection
import rethinkdb as r
from econtextauth import models


class Application:
    """
       Application

       POST - Create a new Application
       GET  - Retrieve an Application
       PUT  - Update an application
       DELETE - Remove an applciation (updates status to deleted - doesn't actually remove the record)
       """
    routes = [
        'applications/application',
        'applications/application/{applicationid}'
    ]

    remodel.connection.pool.configure(db="econtext_users")

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Application(*args)

    def __init__(self, econtext):
        self.econtext = econtext

    def on_post(self, req, resp):
        """
        Create a new Application.
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
        new_application = models.application.application.Application.create_new(name=body.get('name'),
                                                                                description=body.get('description'))

        resp.body = new_application
        return True

    def on_get(self, req, resp, applicationid):
        """
        Retrieve an application specified by id

        :param req:
        :param resp:
        :param applicationid:
        :return:
        """
        new_application = models.application.application.Application.get(applicationid)
        resp.body = new_application
        return True

        # def on_put(self, req, resp, userid):
        #     """
        #     Update a user specified by the userid
        #
        #     This function should receive (key, value) pairs to update.
        #     Ultimately, the user should be retrieved, changed fields
        #     verified, and then those changed fields should be updated in
        #     the database
        #
        #     :param req:
        #     :param resp:
        #     :param userid:
        #     :return:
        #     """
        #     db = self.econtext.get('rethinkdb')
        #     userid = userid or None
        #
        #     # check user exists
        #     # check fields to populate
        #     # update fields
        #     # check_user=r.table('users').get(userid).replace(req.context['body']).run(conn)
        #
        #     # VALIDATE CONTEXT['BODY'] BEFORE UPDATING....
        #     check_user = r.table('users').get(userid).update(req.context['body']).run(db)
        #
        #     resp.body = check_user
        #     return True
        #
        # def on_delete(self, req, resp, userid):
        #     """
        #     Remove a user specified by the userid
        #
        #     The user specified should have the status changed to "deleted"
        #
        #     :param req:
        #     :param resp:
        #     :param userid:
        #     :return:
        #     """
        #
        #     # This will not delete DB entry just change status to Deleted.
        #     # check user exists
        #     # check status?
        #     # change status to deleted
        #
        #     db = self.econtext.get('rethinkdb')
        #     userid = userid or None
        #     check_user = r.table('users').get(userid).update({"status": "deleted"}).run(db)
        #     resp.body = check_user
        #     return True
