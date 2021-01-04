from ..util import get_base_url


class ApplicationParameter(object):
    
    def __init__(self, key=None, datatype=None, default=None, description=None, *args, **kwargs):
        self.key = key
        self.datatype = datatype
        self.default = default
        self.description = description
        self._object = None
    
    def to_dict(self):
        return {
            'key': self.key,
            'datatype': self.datatype,
            'default': self.default,
            'description': self.description
        }
