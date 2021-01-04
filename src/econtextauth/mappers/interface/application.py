from ...models.application import Application


class ApplicationInterface(object):
    
    def to_object(self, group_flag=False, user_flag=False, *args, **kwargs) -> Application:
        """
        Return an Application object from the DB to an Application Model
        
        Be careful with the flags here - it's possible to create recursion
        
        :param group_flag:
        :param user_flag:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_by_uid(uid, group_flag=False, user_flag=False, *args, **kwargs) -> Application:
        """
        Get an Application object hydrated by the DB

        If group_flag is true, hydrate group objects appropriately
        If user_flag is true, hydrate user objects appropriately

        :param uid:
        :param group_flag:
        :param user_flag:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_all(group_flag=False, user_flag=False, limit=25, offset=0, order_by='name', *args, **kwargs) -> set:
        """
        Get Application objects hydrated by the DB

        If group_flag is true, hydrate group objects appropriately
        If user_flag is true, hydrate user objects appropriately

        :param group_flag:
        :param user_flag:
        :param limit:
        :param offset:
        :param order_by:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_some(group_flag=False, user_flag=False, limit=25, offset=0, order_by='name', *args, **kwargs) -> dict:
        """
        Get Application objects hydrated by the DB

        If group_flag is true, hydrate group objects appropriately
        If user_flag is true, hydrate user objects appropriately

        :param group_flag:
        :param user_flag:
        :param limit:
        :param offset:
        :param order_by:
        :param args:
        :param kwargs:
        :return: Returns a dictionary with meta info for paging, and the results
        """
        raise NotImplementedError()
    
    @staticmethod
    def create_from_object(app: Application) -> Application:
        """
        Create a new object, save it, and hydrate new values
        :param app:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def update_from_object(app: Application) -> Application:
        """
        Update an object, and hydrate new values (replaces the old
        object with a new one)
        
        :param app:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def delete_from_object(app: Application) -> bool:
        """
        Delete an object
        
        :param app:
        :return:
        """
        raise NotImplementedError()
