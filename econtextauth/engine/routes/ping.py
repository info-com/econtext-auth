class Ping:
    """
    Simple ping response to determine availability - this will be useful and
    appropriate for working in with other load balancers (e.g. ELB)
    """

    routes = ['ping']

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Ping()

    def on_get(self, req, resp):
        resp.body = {"ping": u'pong'}
        return True
