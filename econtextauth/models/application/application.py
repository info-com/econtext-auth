"""
Application Object

Should contain the following fields:

id
name
description
status
createdAt
modifiedAt
customData
"""
from remodel.models import Model
import rethinkdb as r


class Application(Model):
    has_many = ("User",)

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return self.fields.as_dict()

    def __init__(self, id=None, name=None, description=None, status=None, createdAt=None, modifiedAt=None, customData=None, *args, **kwargs):
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        super(Application, self).__init__(id=id, name=name, description=description, status=status, createdAt=createdAt, modifiedAt=modifiedAt, customData=customData)
