from .data import Data
from ..util import get_base_url


class Organization(object):
    
    def __init__(self, uid=None, name=None, description=None, status=None, created_at=None, modified_at=None, *args, **kwargs):
        self.uid = uid
        self.name = name
        self.status = status
        self.created_at = created_at
        self.modified_at = modified_at
        self.data = set()
        self.users = set()
        self.admins = set()
        self.edits = set()
        self._object = None

    def __hash__(self):
        """
        :return:
        """
        return hash(self.uid)

    def __eq__(self, othr):
        return (self.uid, self.name, self.status, self.created_at, self.modified_at) == \
               (othr.uid, othr.name, othr.status, othr.created_at, othr.modified_at)

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
            'status': self.status or 'DISABLED',
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'data': [x.to_dict() for x in self.data],
            'admins': [x.to_dict_minimal() for x in self.admins],
            'users': [x.to_dict_minimal() for x in self.users],
            'custom_data': self.build_data_dict(),
            'href': '{}/api/organizations/organization/{}'.format(get_base_url(), self.uid),
        }
    
    def to_dict_minimal(self):
        return {
            'id': self.uid,
            'name': self.name,
            'status': self.status or 'DISABLED',
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'data': [x.to_dict() for x in self.data],
            'custom_data': self.build_data_dict(),
            'href': '{}/api/organizations/organization/{}'.format(get_base_url(), self.uid),
        }
    
    def set_name(self, new_name):
        if self.name != new_name:
            self.name = new_name
            self.edits.add(('name', new_name))
        
    def set_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.edits.add(('status', new_status))
    
    def set_data(self, new_data):
        # new_data = [{'key': 'spam', 'value': 'eggs'}, ...]
        new_data = frozenset(Data(**data) for data in new_data if data['key'] != '')
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
        new_data = [{'key': k, 'value': v} for k, v in new_data.items() if k != '']
        return self.set_data(new_data)
