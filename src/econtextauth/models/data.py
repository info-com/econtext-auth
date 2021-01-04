import json


class Data(object):
    
    def __init__(self, key=None, value=None, *args, **kwargs):
        self.key = key
        self.value = value
        self._object = None
    
    def __hash__(self):
        return hash((self.key, json.dumps(self.value)))
    
    def __eq__(self, other):
        return self.key == other.key and self.value == other.value
    
    def __repr__(self):
        return f"<Data key={self.key} value={self.value}>"
    
    def to_dict(self):
        return {
            'key': self.key,
            'value': self.value
        }
