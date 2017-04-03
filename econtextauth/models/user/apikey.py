"""
ApiKey Object

Should contain the following fields:

id
secret
status (ENABLED|DISABLED)
name
description

"""
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

