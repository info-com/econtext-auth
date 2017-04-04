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
from argon2 import PasswordHasher


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
            'secretID': self.fields.secretID
        }

    def __init__(self, name=None, secretID=None, secret=None, status=None, description=None, createdAt=None, *args, **kwargs ):
        createdAt = createdAt or r.now()
        super(ApiKey, self).__init__(name=name, secretID=secretID, secret=secret, status=status, createdAt=createdAt, description=description)

    @staticmethod
    def create_new(name, secret, secretID, description=None, status=None, createdAt=None, modifiedAt=None, *args, **kwargs):
        """
        Create a new ApiKey object

        @todo -- All new APIKEYS need to be associated with an User


        :param secretID:
        :param secret:
        :param name:
        :param description:
        :param status:
        :param createdAt:
        :param modifiedAt:
        :param args:
        :param kwargs:
        :return:
        """
        ph = PasswordHasher()
        if len(secret.strip()) < 6:
            raise Exception("Password must be at least 7 characters long")
        password = ph.hash(secret.strip())
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()

        a = ApiKey(name=name, secret=secret, secretID=secretID, description=description, status=status, createdAt=createdAt,
                 modifiedAt=modifiedAt)
        return a

