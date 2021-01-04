from ...models.data import Data


class DataInterface(object):
    
    def to_object(self, *args, **kwargs) -> Data:
        """
        Return a Data object from the DB to a Data Model

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
