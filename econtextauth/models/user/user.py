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
from argon2 import PasswordHasher


class User(Model):
    has_and_belongs_to_many = ("Application", "Group")
    has_many = ("ApiKey",)

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            # base user data
            'id': self.fields.id,
            'name': self.fields.name,
            'email': self.fields.email,
            'customData': self.fields.customData,
            
            # Extra relations
            'api_keys': list(self.fields.api_keys.all()),
            'groups': list(self.fields.groups.all()),
            'applications': list(self.fields.applications.all())
        }

    def __init__(self, email=None, password=None, name=None, customData=None, status=None, createdAt=None, modifiedAt=None, passwordModifiedAt=None, *args, **kwargs ):
        ph = PasswordHasher()
        if len(password.strip()) < 6:
            raise Exception("Password must be at least 7 characters long")
        password = ph.hash(password.strip())
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        passwordModifiedAt = passwordModifiedAt or r.now()
        super(User, self).__init__(name=name, password=password, email=email, status=status, customData=customData, createdAt=createdAt, modifiedAt=modifiedAt, passwordModifiedAt=passwordModifiedAt)

