from ...models.group import Group as Group


class GroupInterface(object):
    
    def to_object(self, *args, **kwargs) -> Group:
        """
        Return a Group object from the DB to an Group Model

        Be careful with the flags here - it's possible to create recursion

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_by_uid(uid, *args, **kwargs):
        """
        Get a Group object hydrated by the DB

        :param uid:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def get_all(user_flag=False, limit=25, offset=0, order_by='name', *args, **kwargs) -> set:
        """
        Get a set of all Group objects hydrated by the DB
        
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
    def create_from_object(org: Group) -> Group:
        """
        Create a new object, save it, and hydrate new values
        :param org:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def update_from_object(org: Group) -> Group:
        """
        Update an object, and hydrate new values (replaces the old
        object with a new one)
        
        :param org:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def delete_from_object(org: Group) -> bool:
        """
        Delete an object
        
        :param org:
        :return:
        """
        raise NotImplementedError()
