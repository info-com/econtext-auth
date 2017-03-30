"""
Group Object

Should contain the following fields:

id
name
description
status
createdAt
modifiedAt
customData
"""
import datetime
from remodel.models import Model


class Group(Model):
    has_many = ("User",)
    
    def __init__(self, id=None, name=None, description=None, status=None, createdAt=None, modifiedAt=None, customData=None, *args, **kwargs):
        createdAt = createdAt or datetime.datetime.now()
        modifiedAt = modifiedAt or datetime.datetime.now()
        super(Group, self).__init__(id=id, name=name, description=description, status=status, createdAt=createdAt, modifiedAt=modifiedAt, customData=customData)

