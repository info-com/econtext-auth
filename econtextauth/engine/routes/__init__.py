"""
These are the routes to the controllers which provide the interface for
users.
"""

from econtextauth.engine.routes import ping
from econtextauth.engine.routes import users
from econtextauth.engine.routes import applications
from econtextauth.engine.routes import groups
from econtextauth.engine.routes import authenticate


route_classes = [
    ping.Ping,
    users.user.User,
    users.users.Users,
    users.apikey.Apikey,
    users.add.Add,
    users.delete.Delete,
    users.search.Search,
    groups.group.Group,
    groups.groups.Groups,
    authenticate.Authenticate,
    applications.application.Application,
    applications.applications.Applications

]

