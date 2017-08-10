import remodel

class Status:
    """
    Returns status for the Auth API
    """

    routes = ['status']

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Status()

    def on_get(self, req, resp):
        rethink_connection = True
        for conn in remodel.connection.get_conn().gen:
            if not conn.is_open():
                rethink_connection = False
        
        resp.body = {
            "rethinkdb": rethink_connection
        }
        return True
