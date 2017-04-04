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
        return self.fields.as_dict()

    def __init__(self,name=None, description=None, status=None, createdAt=None, modifiedAt=None, customData=None, *args, **kwargs):
        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()
        super(Application, self).__init__(name=name, description=description, status=status, createdAt=createdAt, modifiedAt=modifiedAt, customData=customData)


    @staticmethod
    def create_new(name, description=None, status=None, createdAt=None, modifiedAt=None, customData=None,*args, **kwargs):
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

        createdAt = createdAt or r.now()
        modifiedAt = modifiedAt or r.now()

        a = Application(name=name,customData=customData, description=description, status=status, createdAt=createdAt,
                 modifiedAt=modifiedAt)
        return a

