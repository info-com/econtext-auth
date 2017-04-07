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
import rethinkdb as r


class Application(Model):
    has_and_belongs_to_many = ("User", "Group")
    
    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        mydict = self.fields.as_dict()
        mydict['href'] = '/api/applications/application/{}'.format(self.fields.id)
        return mydict
    
    def __init__(self, name=None, description=None, status=None, createdAt=None, modifiedAt=None, customData=None,
                 *args, **kwargs):
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        super(Application, self).__init__(name=name, description=description, status=status, createdAt=createdAt,
                                          modifiedAt=modifiedAt, customData=customData)
    
    @staticmethod
    def create_new(name, description=None, createdAt=None, modifiedAt=None, customData=None, *args,
                   **kwargs):
        """
        Create a new Apllication object


        :param name:
        :param description:
        :param status:
        :param createdAt:
        :param modifiedAt:
        :param customData:
        :param args:
        :param kwargs:
        :return:
        """
        if Application.already_exists(name):
            raise Exception("An application with that name already exists")
        if Application.empty_req_param(name):
            raise Exception("A name is required for applicaitons")
        status = "ENABLED"
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        
        b = Application(name=name, customData=customData, description=description, status=status, createdAt=createdAt,
                        modifiedAt=modifiedAt)
        b.save()
        return b
    
    @staticmethod
    def already_exists(applciation_name):
        """
        Check to see if a record exists already with this applicaiton name
        :param applciation_name:
        :return boolean:
        """
        if Application.get(name=applciation_name):
            return True
        return False
    
    @staticmethod
    def empty_req_param(req_param):
        if req_param == '' or req_param == None:
            return True
        return False
