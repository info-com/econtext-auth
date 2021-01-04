from ...models.application_parameter import ApplicationParameter as EApplicationParameter


class ApplicationParameterInterface(object):
    
    def to_object(self, *args, **kwargs) -> EApplicationParameter:
        """
        Return an ApplicationParameter object from the DB to an ApplicationParameter Model

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_all_by_application_uid(uid, *args, **kwargs):
        """
        Get a set of ApplicationParameter objects hydrated by the DB

        :param uid:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
