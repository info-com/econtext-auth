from ...models.user import User
from ...models.application import Application
from ...models.group import Group
from typing import List, Set
SetUser = Set[User]


class UserInterface(object):
    
    def to_object(self, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, *args, **kwargs) -> User:
        """
        Return a User object from the DB to an User Model
        
        Be careful with the flags here - it's possible to create recursion

        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_all(organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, limit=25, offset=0, order_by='email', *args, **kwargs) -> SetUser:
        """
        Get all User objects hydrated by the DB
        
        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param limit:
        :param offset:
        :param order_by:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_by_uid(uid, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, *args, **kwargs) -> User:
        """
        Get a User object hydrated by the DB
        
        :param uid:
        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_by_username(username, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, *args, **kwargs) ->User:
        """
        Get a User object hydrated by the DB
        
        :param username:
        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def search(search, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, limit=25, offset=0, order_by='email', *args, **kwargs) -> SetUser:
        """
        Search for Users
        :param search:
        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param limit:
        :param offset:
        :param order_by:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def create_from_object(o: User) -> User:
        """
        Create a new object, save it, and hydrate new values
        :param o:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def update_from_object(o: User) -> User:
        """
        Update an object, and hydrate new values (replaces the old
        object with a new one)
        
        :param o:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def delete_from_object(o: User) -> bool:
        """
        Delete an object
        
        :param o:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def attach_application(o: User, a: Application) -> User:
        """
        Attach an Application to a User
        
        :param o:
        :param a:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def detach_application(o: User, a: Application) -> User:
        """
        Detach an Application from a User - this also removes
        a User from group memberships from that Application
        
        :param o:
        :param a:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def attach_group(o: User, g: Group) -> User:
        """
        Attach a Group to a User
        
        Note: The User must already be a member of the associated Application
        
        :param o:
        :param g:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def detach_group(o: User, g: Group) -> User:
        """
        Detach a Group from a User
        
        :param o:
        :param g:
        :return:
        """
        raise NotImplementedError()
