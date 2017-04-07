"""
ApiKey Object

Should contain the following fields:

id
secret
status (ENABLED|DISABLED)
name
description

"""
import rethinkdb as r
from remodel.models import Model
import uuid
import base64
from argon2 import PasswordHasher

class ApiKey(Model):
    belongs_to = ("User",)

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            'id': self.fields.id,
            'name': self.fields.name,
            'description': self.fields.description,
            'href': '/api/user/apikey/{}'.format(self.fields.id)
        }

    def __init__(self, name=None, secret=None, status=None, description=None, createdAt=None, *args, **kwargs):
        createdAt = createdAt or r.now()
        super(ApiKey, self).__init__(name=name, secret=secret, status=status, createdAt=createdAt,
                                     description=description)

    @staticmethod
    def create_new(name=None, description=None, status=None, createdAt=None, modifiedAt=None, *args, **kwargs):
        """
        Create a new ApiKey object

        @todo -- All new APIKEYS need to be associated with an User


        
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

        secret_uuid = base64.b64encode(str(uuid.uuid1()))
        ph=PasswordHasher
        secret = ph.hash(secret_uuid)
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        status = 'ENABLED'
        a = ApiKey(name=name, secret=secret, description=description, status=status, createdAt=createdAt,
                   modifiedAt=modifiedAt)
        a.save()
        return a
