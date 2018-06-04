import remodel
from econtext.util.falcon.route import Route


class Status(Route):
    """
    Returns status for the Auth API
    """
    
    def on_get(self, req, resp):
        rethink_connection = False
        for conn in remodel.connection.get_conn().gen:
            if conn.is_open():
                rethink_connection = True
                break
        
        if not rethink_connection:
            raise Exception("Could not connect to RethinkDB database")
        
        resp.body = {
            "rethinkdb": rethink_connection
        }
        return True
