import rethinkdb as r
import remodel

remodel.connection.pool.configure(db="econtext_users")
from econtextauth import models
from econtextauth.engine import bin

conn = r.connect(db='econtext_users')

bin.rethink.create_tables(conn)
bin.rethink.create_indexes(conn)

v = models.user.user.User(name="mark marnelli", password="somebcrypt", email="someemail@address.com")
v.save()

# get the user using the id
# u = models.user.user.User.get('6379fec4-cba1-4c3a-ad1d-fc2782377111')
# u['api_keys'].add(models.user.apikey.ApiKey(name="eContext API Key", password="My API Key"))
# u.save()

# This is our base application - you must be a member to access auth.econtext.com
app_auth = models.application.application.Application(name='eContext Auth',
                                                      description='eContext Authentication/Authorization Application')
app_auth.save()

app_api = models.application.application.Application(name='eContext API', description='eContext API for Classification')
app_auth.save()

group_api = models.group.group.Group(name='Standard API User', description="Standard users of the eContext API",
                                     customData={
                                         "classify_limit": 10,
                                         "tier_depth": 9
                                     })
group_api.save()

group_api_admin = models.group.group.Group(name='Standard API User', description="Standard users of the eContext API",
                                           customData={
                                               "_no_encrypt": True,
                                               "company_id": 9999999,
                                               "tier_depth": 9999
                                           })
group_api_admin.save()
