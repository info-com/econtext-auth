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
import logging
log=logging.getLogger('econtext')



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
    def create_new(name=None, description=None, createdAt=None, modifiedAt=None, *args, **kwargs):
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
        ph=PasswordHasher()
        secret = ph.hash(secret_uuid)
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        status = 'ENABLED'
        a = ApiKey(name=name, secret=secret, description=description, status=status, createdAt=createdAt,
                   modifiedAt=modifiedAt)
        a.save()
        return a


    @staticmethod
    def edit_apikey(update_apikey,name=None,description=None,status=None,customData=None, *args, **kwargs):
        if kwargs is not None:
            ap = update_apikey
            log.debug(name)
            log.debug(description)
            log.debug(status)
        
            if name != None and (name != ap['name']):
            
                if ApiKey.empty_req_param(name):
                    raise Exception('A name is required for apikey')
                if ApiKey.already_exists(name):
                    raise Exception("An apikey with that name address already exists")
                ap['name'] = name
        
            if description != None:
                ap['description'] = description
        
            if status != None:
                ap['status'] = status
            if customData != None:
                ap['customData'] = customData
        
            ap.save()
            return ap

    @staticmethod
    def already_exists(apikey_name):
        """
        Check to see if a record exists already with this applicaiton name
        :param applciation_name:
        :return boolean:
        """
        if ApiKey.get(name=apikey_name):
            return True
        return False

    @staticmethod
    def empty_req_param(req_param):
        if req_param == '' or req_param == None:
            return True
        return False
