from ..util import get_base_url
from .data import Data


class Group(object):
    
    def __init__(self, uid=None, name=None, description=None, status=None, application=None, created_at=None, modified_at=None, *args, **kwargs):
        self.uid = uid
        self.name = name
        self.description = description
        self.status = status
        self.application = application
        self.created_at = created_at
        self.modified_at = modified_at
        self.data = set()
        self.edits = set()
        self._object = None
    
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
            'application': self.application,
            'status': self.status or 'DISABLED',
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'data': [x.to_dict() for x in self.data],
            'custom_data': self.build_data_dict(),
            'href': '{}/api/groups/group/{}'.format(get_base_url(), self.uid),
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
