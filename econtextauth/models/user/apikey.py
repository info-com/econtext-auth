"""
ApiKey Object

Should contain the following fields:

id
secret
status (ENABLED|DISABLED)
name
description
secretID

"""
import rethinkdb as r
from remodel.models import Model


class ApiKey(Model):
    belongs_to = ("User", )

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            'id': self.fields.id,
            'name': self.fields.name,
            'password': self.fields.password
        }

    def __init__(self, name=None, secretID=None, secret=None, status=None, description=None, createdAt=None, *args, **kwargs ):
        createdAt = createdAt or r.now()
        super(ApiKey, self).__init__(name=name, password=secretID, email=secret, status=status, createdAt=createdAt, description=description)

