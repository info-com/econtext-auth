import neomodel
from econtext.util.falcon.route import Route


class Status(Route):
    """
    Returns status for the Auth API
    """
    
    def on_get(self, req, resp):
        mapper = self.meta.get('mapper')
        mapper_connection = mapper.check_connection()
        resp.body = {
            "mapper-name": mapper.get_name(),
            "mapper-connection": mapper_connection
        }
        return True
