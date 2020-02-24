from gevent import monkey; monkey.patch_all()

import argparse
import remodel.connection
from multiprocessing import cpu_count
from econtext.util.config import load_config, update_config, config_get
from econtext.util.falcon import get_app, setup_app, update_app_middleware
from econtext.util.falcon.route import Routes
from econtext.util.gunicorn.app import StandaloneApplication
from econtext.util.log import log, log_add_stream_handler
from econtextauth.engine.middleware.econtext.authenticator import Authenticator
import falcon
import json
from .auth_cache import AuthCache


################################################################################
# Base settings (where to find files)
################################################################################
default_config = {
    'rethinkdb_host': 'localhost',
    'rethinkdb_port': '28015',
    'base_url': 'localhost:8000'
}


def prepare_econtext_objects(config):
    rethinkdb_host = config_get(config, 'engine', 'rethinkdb_host')
    rethinkdb_port = config_get(config, 'engine', 'rethinkdb_port', 28015)
    log.info("Connecting to RethinkDB at {}:{}".format(rethinkdb_host, rethinkdb_port))
    remodel.connection.pool.configure(host=rethinkdb_host, port=rethinkdb_port, db="econtext_users")
    
    auth_cache = AuthCache(size=50, ip_attempt_limit=20)
    
    route_options = {
        "application_id": config_get(config, 'engine', 'application_id'),
        "auth_cache": auth_cache
    }
    return route_options


def setup_routes(econtext_objects):
    """
    Setup our routes here - econtext_objects are passed in to the
    Route constructors and provide access to common objects in
    each route (think db connections, a taxonomy object, etc)

    In this example, there are two routes that point to the HelloWorld
    route.  This is allowed, but you should be very careful here.
    The reason for doing it this way is that a single Route can handle
    `on_get` and `on_post`.  However, generally, the `on_get` would
    be the one that is pointing to `/hello/{name}`.  However, you could
    also potentially POST to `/hello/{name}` and get behaviour that
    you're not quite expecting.  Be careful!

    @see http://falcon.readthedocs.io/en/stable/user/tutorial.html

    :param econtext_objects:
    :return:
    """
    from .routes.applications.application import Application
    from .routes.applications.applications import Applications
    from .routes.applications.groups import Groups as ApplicationGroups
    from .routes.applications.users import Users as ApplicationUsers
    from .routes.groups.group import Group
    from .routes.groups.groups import Groups
    from .routes.groups.users import Users as GroupUsers
    from .routes.users.apikey import Apikey as UsersApikey
    from .routes.users.application import Application as UsersApplication
    from .routes.users.group import Group as UsersGroup
    from .routes.users.search import Search as UsersSearch
    from .routes.users.user import User
    from .routes.users.users import Users
    from .routes.authenticate import Authenticate
    from .routes.status import Status
    
    routes = Routes(econtext_objects)
    routes.create_route(Application, 'applications/application')
    routes.create_route(Application, 'applications/application/{appid}')
    routes.create_route(Applications, 'applications')
    routes.create_route(ApplicationGroups, 'applications/application/{appid}/groups')
    routes.create_route(ApplicationUsers, 'applications/application/{appid}/users')
    routes.create_route(Group, 'groups/group')
    routes.create_route(Group, 'groups/group/{groupid}')
    routes.create_route(Groups, 'groups')
    routes.create_route(GroupUsers, 'groups/group/{groupid}/users')
    routes.create_route(UsersApikey, 'users/user/{userid}/apikey')
    routes.create_route(UsersApikey, 'users/user/{userid}/apikey/{apikeyid}')
    routes.create_route(UsersApplication, 'users/user/{userid}/application/{appid}')
    routes.create_route(UsersGroup, 'users/user/{userid}/group/{groupid}')
    routes.create_route(UsersSearch, 'users/search/{search}')
    routes.create_route(User, 'users/user')
    routes.create_route(User, 'users/user/{userid}')
    routes.create_route(Users, 'users')
    routes.create_route(Authenticate, 'authenticate')
    routes.create_route(Status, 'status')
    
    return routes


def error_serializer(req, resp, exception):
    """
    Don't actually serialize the exception - just return the dictionary that we
    want.  The response body itself should be serialized in our middleware.

    @see econtext.engine.middleware.econtext.econtext
    :type resp: falcon.Response

    """
    log.debug("error_serializer")
    resp.body = {"error": exception.to_dict()}
    log.debug(resp.body)
    if isinstance(exception, falcon.HTTPUnauthorized):
        resp.body = json.dumps(resp.body).encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description='Start the eContext Classification Engine.')
    parser.add_argument("--config", dest="config_config_file", default="/etc/econtext/auth/econtextauth.ini",
                        help="Configuration file", metavar="PATH")
    parser.add_argument("-v", dest="config_verbose", action="count", default=0, help="Be more or less verbose")
    options = parser.parse_args()

    log_add_stream_handler(options.config_verbose)
    config = load_config(options.config_config_file, default_config)
    for section in {'server', 'engine', 'config'}.difference(set(config.sections())):
        config.add_section(section)

    del options.config_config_file
    del options.config_verbose

    config_updates = dict()
    for k, v in options.__dict__.items():
        if v is not None:
            section, key = k.split("_", 1)
            if section not in config_updates:
                config_updates[section] = dict()
            config_updates[section][key] = str(v)
    update_config(config, config_updates)

    app = get_app(config_get(config, 'config', 'access_log'), config_get(config, 'config', 'error_log'), middlewares=[Authenticator(config_get(config, 'engine', 'application_id'))])
    app.set_error_serializer(error_serializer)
    econtext_objects = prepare_econtext_objects(config)
    routes = setup_routes(econtext_objects)
    setup_app(app, routes, route_prefix='api')

    server_config = dict(config.items('server'))
    options = {
        'worker_class': 'gevent',
        'bind': "{}:{}".format(server_config.get('host', '0.0.0.0'), server_config.get('port', '8000')),
        'workers': int(server_config.get('workers', cpu_count())),
        'threads': int(server_config.get('threads', 100)),
        'max_requests': server_config.get('max_requests', 1000),
        'graceful_timeout': server_config.get('graceful_timeout', 5),
        'pidfile': server_config.get('pidfile', '/var/run/econtextauth-engine.pid'),
        'preload_app': True,

        # CALLBACKS
        # 'post_fork': post_fork,
        # 'worker_exit': worker_exit,
        # 'post_request': post_request,
        # 'pre_request': pre_request,
        # 'worker_abort': worker_oops
    }
    try:
        StandaloneApplication(app, options).run()
    except Exception:
        log.exception("Caught an Exception...")


if __name__ == '__main__':
    main()
