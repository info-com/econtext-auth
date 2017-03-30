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

