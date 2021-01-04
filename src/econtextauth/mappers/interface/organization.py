from ...models.organization import Organization


class OrganizationInterface(object):
    
    def to_object(self, user_flag=False, *args, **kwargs) -> Organization:
        """
        Return an Organization object from the DB to an Organization Model

        Be careful with the flags here - it's possible to create recursion

        :param user_flag:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_by_uid(uid, user_flag=False, *args, **kwargs) -> Organization:
        """
        Get an Organization object hydrated by the DB

        :param uid:
        :param user_flag:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def get_all(user_flag=False, limit=25, offset=0, order_by='name', *args, **kwargs) -> set:
        """
        Get a set of all Organization objects hydrated by the DB
        
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
    def create_from_object(org: Organization) -> Organization:
        """
        Create a new object, save it, and hydrate new values
        :param org:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def update_from_object(org: Organization) -> Organization:
        """
        Update an object, and hydrate new values (replaces the old
        object with a new one)
        
        :param org:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def delete_from_object(org: Organization) -> bool:
        """
        Delete an object
        
        :param org:
        :return:
        """
        raise NotImplementedError()
