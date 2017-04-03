import logging
log = logging.getLogger('econtext')
from pprint import pprint
import remodel.utils
import remodel.connection
import rethinkdb as r



class User:
    """
    Users

    POST - Create a new user
    GET  - Retrieve a user
    PUT  - Update a user
    DELETE - Remove a user (updates status to deleted - doesn't actually remove the record)
    """
    routes = [
        'users/user',
        'users/user/{userid}'
    ]
    remodel.connection.pool.configure(db="test")
    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return User(*args)
    
    def __init__(self, econtext):
        self.econtext = econtext



    def on_post(self, req, resp):
        """
        Create a new User.
        
        Requires, at minimum, a username(email), and password.  In
        order to actually be used to login anywhere, we also need
        membership in an application.
        
        A globally unique id should also be generated for each new user
        and is used as the primary key in the database.  Existing ids
        formats may be different from these.
        
        :todo work out the id structure
        
        :param req:
        :param resp:
        :return:
        """

        #this_user=User.create()
        #self.econtext.get('rethinkdb')
        db=self.econtext.get('rethinkdb')
        body= req.context['body']
        #print body['password']
        #print body['email']
        try:
            db_json={
                "email":body['email'],
                "password":body['password']
            }
        except KeyError as e:
            print "must include necessary values"
            resp.body = "Could not create user, missing fields."
            return False
        test_instert=r.table('users').insert(db_json).run(db)

        resp.body=test_instert
        return True
    
    def on_get(self, req, resp, userid):
        """
        Retrieve a user specified by id
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        #assert userid is id
        db=self.econtext.get('rethinkdb')
        userid = userid or None
        #user=User(userid)
        #print 'user', user, pprint(vars(user))
        # print(r.table('accounts')
        #         .order_by(r.desc('id')).run(conn))
        #return_body=r.table('accounts').get("35528c0a-4fd6-4b16-8b0e-7ac41a9ef398").run(conn)

        test_body=r.table('users').get(userid).run(db)

        print userid
        print test_body
        #pprint(vars(db))

        resp.body=test_body
        return True
    
    def on_put(self, req, resp, userid):
        """
        Update a user specified by the userid
        
        This function should receive (key, value) pairs to update.
        Ultimately, the user should be retrieved, changed fields
        verified, and then those changed fields should be updated in
        the database
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """
        db=self.econtext.get('rethinkdb')
        userid = userid or None


        #check user exists
        #check fields to populate
        #update fields
        #check_user=r.table('users').get(userid).replace(req.context['body']).run(conn)

        #VALIDATE CONTEXT['BODY'] BEFORE UPDATING....
        check_user = r.table('users').get(userid).update(req.context['body']).run(db)


        resp.body = check_user
        return True

    def on_delete(self, req, resp, userid):
        """
        Remove a user specified by the userid
        
        The user specified should have the status changed to "deleted"
        
        :param req:
        :param resp:
        :param userid:
        :return:
        """

        #This will not delete DB entry just change status to Deleted.
        # check user exists
        # check status?
        # change status to deleted

        db = self.econtext.get('rethinkdb')
        userid = userid or None
        check_user = r.table('users').get(userid).update({"status":"deleted"}).run(db)
        resp.body = check_user
        return True