"""
These are the routes to the controllers which provide the interface for
users.
"""

from econtextauth.engine.routes import ping
from econtextauth.engine.routes import users
from econtextauth.engine.routes import applications
from econtextauth.engine.routes import groups
from econtextauth.engine.routes import authenticate
from econtextauth.engine.routes import showusers
from econtextauth.engine.routes import showgroups
from econtextauth.engine.routes import showapplications


route_classes = [
    ping.Ping,
    users.user.User,
    users.apikey.Apikey,
    users.search.Search,
    groups.group.Group,
    authenticate.Authenticate,
    applications.application.Application,
    showgroups.Showgroups,
    showapplications.Showapplications,
    showusers.Showusers
]
