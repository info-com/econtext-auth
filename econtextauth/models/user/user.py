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
import datetime
import remodel.utils
import remodel.connection


remodel.connection.pool.configure(db="test")

class User(Model):
    belongs_to = ("Application","Group",)
    #belongs_to = ("Group",)
    has_many = ("ApiKey",)

    # def get(self):
    #     u"""
    #     Returns this object as a JSON object
    #     """
    #     return {
    #         "id":self.id,
    #         "name":self.name,
    #         "createdAt":self.createdAt,
    #         "email":self.email
    #     }

    @property
    def json(self):
        u"""
        Returns this object as a JSON object
        """
        return {
            "id":self.id,
            "name":self.name
        }

    def __init__(self,id=None, name=None, password=None,email=None, status=None, customData=None, createdAt=None, modifiedAt=None, passwordModifiedAt=None,*args,**kwargs ):
        createdAt=createdAt or datetime.datetime.now()
        modifiedAt=modifiedAt or datetime.datetime.now()
        super(User,self).__init__(id=id,name=name,password=password,email=email,status=status, customData=customData,createdAt=createdAt,modifiedAt=modifiedAt,passwordModifiedAt=passwordModifiedAt)

