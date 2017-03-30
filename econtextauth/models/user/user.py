"""
Basic User object

Should contain the following fields:

id
email
password (hashed)
name
status (ENABLED|DISABLED)
customData (a JSON object)
createdAt (2017-02-10T21:32:18.042Z)
modifiedAt (2017-02-10T21:32:18.042Z)
passwordModifiedAt (2017-02-10T21:32:18.042Z)

"""
from remodel.models import Model


class User(Model):
    belongs_to = ("Application",)
    belongs_to = ("Group",)
    has_many = ("ApiKey",)

