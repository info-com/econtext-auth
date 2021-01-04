from .application_parameter import ApplicationParameter
from .data import Data
from ..util import get_base_url


class Application(object):
    
    def __init__(self, uid=None, name=None, description=None, jwt_secret=None, status=None, created_at=None, modified_at=None, *args, **kwargs):
        self.uid = uid
        self.name = name
        self.description = description
        self.jwt_secret = jwt_secret
        self.status = status
        self.created_at = created_at
        self.modified_at = modified_at
        self.parameters = set()
        self.data = set()
        self.groups = set()
        self.users = set()
        self.edits = set()
        self._object = None
    
    def __hash__(self):
        """
        :return:
        """
        return hash(self.uid)
    
    def __eq__(self, other):
        return (self.uid, self.name, self.description, self.jwt_secret, self.status, self.created_at, self.modified_at) == \
               (other.uid, other.name, other.description, other.jwt_secret, other.status, other.created_at, other.modified_at)
    
    def build_data_dict(self):
        """
        Return the data fields as a dictionary. This maintains backward
        compatibility with an older version, but should not be relied
        on moving forward. Use the data list instead.
        :return:
        """
        return {d.key: d.value for d in self.data}
    
    def to_dict(self):
        return {
            'id': self.uid,
            'name': self.name,
            'description': self.description,
            'jwt_secret': self.jwt_secret,
            'status': self.status or 'DISABLED',
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'data': [x.to_dict() for x in self.data],
            'parameters': [x.to_dict() for x in self.parameters],
            'custom_data': self.build_data_dict(),
            'href': '{}/api/applications/application/{}'.format(get_base_url(), self.uid)
        }
    
    def set_name(self, new_name):
        if self.name != new_name:
            self.name = new_name
            self.edits.add(('name', new_name))
    
    def set_description(self, new_description):
        if self.description != new_description:
            self.description = new_description
            self.edits.add(('description', new_description))
    
    def set_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.edits.add(('status', new_status))
    
    def set_jwt_secret(self, new_jwt_secret):
        if self.jwt_secret != new_jwt_secret:
            self.jwt_secret = new_jwt_secret
            self.edits.add(('jwt_secret', new_jwt_secret))
    
    def set_data(self, new_data):
        # new_data = [{'key': 'spam', 'value': 'eggs'}, ...]
        new_data = frozenset(Data(**data) for data in new_data)
        if self.data != new_data:
            self.data = new_data
            self.edits.add(('data', new_data))
    
    def set_custom_data(self, new_data):
        """
        custom_data comes in as a dictionary instead of a list. So,
        first, we change this into a list, and then submit it.
        
        :param new_data:
        :return:
        """
        new_data = [{'key': k, 'value': v} for k, v in new_data.items()]
        return self.set_data(new_data)
    
    def set_parameters(self, new_parameters):
        # new_data = [{'key': 'spam', 'datatype': 'str', 'default': 'eggs', 'description': 'spam and eggs'}, ...]
        new_params = {ApplicationParameter(**param) for param in new_parameters}
        if self.parameters != new_params:
            self.parameters = new_params
            self.edits.add(('parameters', new_params))
