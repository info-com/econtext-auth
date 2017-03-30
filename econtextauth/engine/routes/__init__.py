"""
These are the routes to the controllers which provide the interface for
users.
"""

from econtextauth.engine.routes import ping
from econtextauth.engine.routes import users
from econtextauth.engine.routes import applications
from econtextauth.engine.routes import groups

route_classes = [
    ping.Ping,
    users.user.User,
    users.search.Search,
    # applications.Appliation,
    # groups.Group,
]
