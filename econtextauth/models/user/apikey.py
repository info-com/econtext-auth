"""
ApiKey Object

Should contain the following fields:

id
secret
status (ENABLED|DISABLED)
name
description

"""
import uuid
import random
import base64
import logging
from remodel.models import Model, before_save
from rethinkdb import now
from argon2 import PasswordHasher
log = logging.getLogger('econtext')


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

    @staticmethod
    def create_new(user, name=None, description=None, status=None, id_=None, secret=None, *args, **kwargs):
        """
        Create a new ApiKey object
        
        The return object contains a plaintext version of the secret.
        This is the last time that you can see the unhashed version, so
        please be sure to save it somewhere.
        
        :return:
        """
        if not user:
            raise Exception("You must have a valid user to create an ApiKey")
        
        ph = PasswordHasher()
        if not id_:
            id_ = ApiKey.generate_25_char_id()
        if not secret:
            secret = base64.b64encode(str(uuid.uuid4()))
        
        secret_hash = ph.hash(secret)
        created_at = now()
        status = status or 'ENABLED'
        a = ApiKey(id=id_, name=name, description=description, secret=secret_hash, status=status, created_at=created_at)
        a.save()
        
        # Save the API Key to the user
        user['api_keys'].add(a)
        user.save()
        
        a['secret'] = secret
        return a

    def update_model(self, updates=None):
        """
        Updates a User

        :return:
        """
        if updates is None:
            return
        
        updates.pop('created_at', None)
        for k, v in updates.items():
            if k in ('name', 'description', 'status'):
                self[k] = v
        self.save()
    
    @before_save
    def update_modification_time(self):
        """
        Update the modified_at parameter whenever we save

        :return:
        """
        self.fields.modified_at = now()
        return True
    
    @staticmethod
    def generate_25_char_id():
        x = 0
        while True:
            api_id = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(25))
            if not ApiKey.get(api_id):
                return api_id
            x += 1
            if x > 10:
                raise Exception("Couldn't generate a unique apikey id in 10 tries.  Please try again")
