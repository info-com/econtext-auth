"""
These are the routes to the controllers which provide the interface for
users.
"""

from econtextauth.engine.routes import ping
from econtextauth.engine.routes import users
from econtextauth.engine.routes import applications
from econtextauth.engine.routes import groups
from econtextauth.engine.routes import authenticate
from econtextauth.engine.routes import test


route_classes = [
    ping.Ping,
    test.Test,
    authenticate.Authenticate,
    
    applications.application.Application,
    applications.applications.Applications,
    applications.users.Users,
    applications.groups.Groups,
    groups.group.Group,
    groups.groups.Groups,
    groups.users.Users,
    users.user.User,
    users.users.Users,
    users.apikey.Apikey,
    users.application.Application,
    users.group.Group,
    users.search.Search
]

