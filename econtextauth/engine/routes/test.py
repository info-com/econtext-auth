class Test:
    """
    Testing response
    """

    routes = ['test']

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Test()

    def on_get(self, req, resp):
        raise Exception("Just throwing an exception to test")
        return True
