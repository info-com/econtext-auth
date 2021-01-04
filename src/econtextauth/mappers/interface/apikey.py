from ...models.apikey import ApiKey as EApiKey


class ApiKeyInterface(object):
    
    def to_object(self, *args, **kwargs) -> EApiKey:
        """
        Return an ApiKey object from the DB to an ApiKey Model

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_by_key(key, *args, **kwargs) -> EApiKey:
        """
        Get an ApiKey object hydrated by the DB

        :param key:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def create_from_object(o: EApiKey) -> EApiKey:
        """
        Create a new object, save it, and hydrate new values
        :param o:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def delete_from_object(o: EApiKey) -> bool:
        """
        Delete an object
        
        :param o:
        :return:
        """
        raise NotImplementedError()
    
