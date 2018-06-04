class Test:
    """
    Testing response
    """
    
    def on_get(self, req, resp):
        raise Exception("Just throwing an exception to test")
        return True
