import logging

log = logging.getLogger('econtext')
from econtextauth import models


class Search:
    """
    Search

    GET - Search for a user
    """
    routes = [
        'users/search/{search}',
    ]

    @staticmethod
    def get_route_constructor(*args, **kwargs):
        return Search(*args)

    def __init__(self, econtext):
        self.econtext = econtext

    def on_get(self, req, resp, search):
        """
        Retrieve a list of users that match the provided search term

        :type search: str
        
        :param req:
        :param resp:
        :param search: A string to search for
        :return:
        """

        """
        regex? partial match? which fields to compare?
        
        """

        # user_search=models.user.user.User.getAll()
        # user_search=models.user.user.User.objects.query.filter((lambda user: user['email'].match('test2jkfkdjaklfjalksfj')) or (lambda user: user['name'].match('ma'))).run()
        # user_search = models.user.user.User.objects.query.filter(
        #     lambda user: (user['name'].match(search)) | (user['email'].match(search))).run()
        #
        # user_search2=models.user.user.User.objects.query.filter(
        #     lambda user: (user['name'].match(search)) | (user['email'].match(search))).run()


        # user_search_nested.append(models.user.user.User.objects.query.filter(lambda user: (user['customData'].match(search))).map(lambda user:
        #                                                                                             {'id': user['id'],
        #                                                                                              'name': user[
        #                                                                                                  'name'],
        #                                                                                              'email': user[
        #                                                                                                  'email']}).run())

        # user_search_nested = []
        #
        # user_search_nested.append(models.user.user.User.objects.query.filter(lambda user : user['customData'].match(search)).run())
        # for a in user_search_nested:
        #     log.debug(a)
        #
        #
        #
        #
        #
        #
        # # user_search0.append(models.user.user.User.objects.query.filter(
        # #     lambda user: (user['email'].match(search))).run())
        #
        #
        # #     user_search4=models.user.user.User.objects.query.map(lambda user:
        # # { 'name': user['name'], 'id': user['id'] }).run()
        #
        # # log.debug(user_search)
        # # log.debug(user_search2)
        # log.debug(user_search_nested)
        #

        # user.user.User.objects.query.filter(
        #     lambda user: (user['email'].match('hi')) | (user['name'].match('hi')) | (user['id'].match('hi'))).run()
        user_search0 = []
        user_search0.append(models.user.user.User.objects.query.filter(
            lambda user: (user['email'].match(search))).map(lambda user:
                                                            {'id': user['id'], 'name': user['name'],
                                                             'email': user['email']}).run())

        user_search0.append(
            models.user.user.User.objects.query.filter(lambda user: (user['email'].match(search))).map(lambda user:
                                                                                                       {'id': user[
                                                                                                           'id'],
                                                                                                        'name': user[
                                                                                                            'name'],
                                                                                                        'email': user[
                                                                                                            'email']}).run())
        user_search0.append(
            models.user.user.User.objects.query.filter(lambda user: (user['id'].match(search))).map(lambda user:
                                                                                                    {'id': user['id'],
                                                                                                     'name': user[
                                                                                                         'name'],
                                                                                                     'email': user[
                                                                                                         'email']}).run())

        for each_result in user_search0:
            log.debug(each_result)
        log.debug(user_search0)
        resp.body = user_search0
        return True
