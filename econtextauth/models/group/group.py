"""
Group Object

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


class Group(Model):
    has_and_belongs_to_many = ("User", "Application")

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        mydict=self.fields.as_dict()
        mydict['href']='/api/groups/group/{}'.format(self.fields.id)
        
        return mydict

    def __init__(self, name=None, description=None, status=None, createdAt=None, modifiedAt=None, customData=None,
                 *args, **kwargs):
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        status = status or 'ENABLED'
        super(Group, self).__init__(name=name, description=description, status=status, createdAt=createdAt,
                                    modifiedAt=modifiedAt, customData=customData)

    @staticmethod
    def create_new(name, description=None, customData=None, status=None, createdAt=None, modifiedAt=None, *args,
                   **kwargs):
        """
        Create a new Group object


        :param name:
        :param customData:
        :param description:
        :param status:
        :param createdAt:
        :param modifiedAt:
        :param args:
        :param kwargs:
        :return:
        """

        status="ENABLED"
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        if Group.empty_req_param(name):
            raise Exception('param cannot be none')
        if Group.already_exists(name):
            raise Exception("A group with that name address already exists")
        g = Group(name=name, customData=customData, description=description, status=status, createdAt=createdAt,
                  modifiedAt=modifiedAt)
        g.save()
        return g

    @staticmethod
    def already_exists(group_name):
        """
        Check to see if a record exists already with this applicaiton name
        :param applciation_name:
        :return boolean:
        """
        if Group.get(name=group_name):
            return True
        return False
    
    @staticmethod
    def empty_req_param(req_param):
        if req_param == '' or req_param == None:
            return True
        return False
        