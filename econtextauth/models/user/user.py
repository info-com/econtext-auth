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
import rethinkdb as r
from remodel.models import Model


class User(Model):
    belongs_to = ("Application", "Group")
    has_many = ("ApiKey",)

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            'id': self.fields.id,
            'name': self.fields.name,
            'email': self.fields.email,
            'customData': self.fields.customData,
            'api_keys': list(self.fields.api_keys.all())
        }

    def __init__(self, name=None, password=None, email=None, status=None, customData=None, createdAt=None, modifiedAt=None, passwordModifiedAt=None, *args, **kwargs ):
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        super(User, self).__init__(name=name, password=password, email=email, status=status, customData=customData, createdAt=createdAt, modifiedAt=modifiedAt, passwordModifiedAt=passwordModifiedAt)

