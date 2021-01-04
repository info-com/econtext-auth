from ..util import get_base_url


class ApiKey(object):
    
    def __init__(self, key=None, secret=None, name=None, description=None, status=None, created_at=None, modified_at=None, *args, **kwargs):
        self.key = key
        self.secret = secret
        self.name = name
        self.description = description
        self.status = status
        self.created_at = created_at
        self.modified_at = modified_at
        self.user = None  # should be a type of .user.User
        self._object = None
        self.edits = set()
    
    def to_dict_minimal(self):
        return {
            'id': self.key,
            'name': self.name,
            'description': self.description,
            'status': self.status or 'DISABLED',
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'href': '{}/api/users/user/{}/apikey/{}'.format(get_base_url(), self.user.uid, self.key)
        }
    
    def to_dict(self):
        return {
            'id': self.key,
            'secret': self.secret,
            'name': self.name,
            'description': self.description,
            'status': self.status or 'DISABLED',
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'href': '{}/api/users/user/{}/apikey/{}'.format(get_base_url(), self.user.uid, self.key)
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
