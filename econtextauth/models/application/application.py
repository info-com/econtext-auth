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


class Application(Model):
    has_many = ("User",)
