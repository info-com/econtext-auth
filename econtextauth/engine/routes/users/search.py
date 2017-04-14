from econtextauth.models.user import user, apikey
import logging

log = logging.getLogger('econtext')


class Search:
    """
    Search
    
    GET - Search for a user
    """
    routes = ['users/search/{search}', ]
    
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
        
        # Grab users based on email, name, or id
        users = set([user.User(**x) for x in user.User.objects.query.filter(
            lambda x:
                (x['email'].match('(?i){}'.format(search))) |
                (x['name'].match('(?i){}'.format(search))) |
                (x['id'].match('(?i){}'.format(search)))
        ).run()])
        
        # Grab users based on API key id (this is the easiest way to match up a user from weblogs
        apikey_users = set([user.User.get(key['user_id']) for key in apikey.ApiKey.objects.query.filter(
            lambda x: (x['id'].match('(?i){}'.format(search)))
        ).pluck('user_id').run()])
        for apikey_user in apikey_users:
            users.add(apikey_user)
        
        # Grab users based on fields in the custom_data field of a user
        custom_data_users = set([
            user.User.get(key['id']) for key in user.User.objects.query.filter(
                lambda x:
                (x['custom_data']['company_name'].match('(?i){}'.format(search)))
            ).run()
        ])
        users.update(custom_data_users)

        resp.body = list(users)
        return True
