from gevent import monkey; monkey.patch_all()

import argparse
from multiprocessing import cpu_count
from econtext.util.config import load_config, update_config, config_get
from econtext.util.falcon import get_app, setup_app, update_app_middleware
from econtext.util.falcon.route import Routes
from econtext.util.gunicorn.app import StandaloneApplication
from econtext.util.log import log, log_add_stream_handler
from ..engine.middleware.econtext.authenticator import Authenticator
import falcon
import json
from ..mappers import neo4j
from neomodel import config as neo_config
from ..engine.auth_cache import AuthCache


################################################################################
# Base settings (where to find files)
################################################################################
default_config = {
    'rethinkdb_host': 'localhost',
    'rethinkdb_port': '28015',
    'base_url': 'localhost:8000'
}


def prepare_route_objects(config):
    """
    Initialize the mapper here, as well as the cache
    
    Mapper should be config based with an initializer for each
    
    :param config:
    :return:
    """
    auth_cache = AuthCache(size=50, ip_attempt_limit=20)
    
    mapper_name = config_get(config, 'econtextauth', 'mapper')
    mapper_uri = config_get(config, 'econtextauth', 'mapper_uri')
    mapper = None
    
    if mapper_name == 'neo4j':
        neo_config.DATABASE_URL = mapper_uri
        mapper = neo4j
    
    route_options = {
        'application_id': config_get(config, 'econtextauth', 'application_id'),
        'auth_cache': auth_cache,
        'mapper': mapper
    }
    return route_options


def setup_routes(route_objects):
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

    :param route_objects:
    :return:
    """
    from ..engine.routes.applications.application import Application
    from ..engine.routes.applications.applications import Applications
    from ..engine.routes.applications.groups import Groups as ApplicationGroups
    from ..engine.routes.applications.users import Users as ApplicationUsers
    from ..engine.routes.organizations.organization import Organization
    from ..engine.routes.organizations.organizations import Organizations
    from ..engine.routes.organizations.users import Users as OrganizationsUsers
    from ..engine.routes.groups.group import Group
    from ..engine.routes.groups.groups import Groups
    from ..engine.routes.groups.users import Users as GroupUsers
    from ..engine.routes.users.apikey import ApiKey as UsersApiKey
    from ..engine.routes.users.application import Application as UsersApplication
    from ..engine.routes.users.group import Group as UsersGroup
    from ..engine.routes.users.search import Search as UsersSearch
    from ..engine.routes.users.user import User
    from ..engine.routes.users.users import Users
    from ..engine.routes.authenticate import Authenticate
    # from ..engine.routes.status import Status
    
    routes = Routes(route_objects)
    # Applications
    routes.create_route(Application, 'applications/application')
    routes.create_route(Application, 'applications/application/{appid}')
    routes.create_route(Applications, 'applications')
    routes.create_route(ApplicationGroups, 'applications/application/{appid}/groups')
    routes.create_route(ApplicationUsers, 'applications/application/{appid}/users')
    
    # Organizations
    routes.create_route(Organization, 'organizations/organization')
    routes.create_route(Organization, 'organizations/organization/{orgid}')
    routes.create_route(Organizations, 'organizations')
    routes.create_route(OrganizationsUsers, 'organizations/organization/{orgid}/users')
    routes.create_route(Group, 'groups/group')
    routes.create_route(Group, 'groups/group/{groupid}')
    routes.create_route(Groups, 'groups')
    routes.create_route(GroupUsers, 'groups/group/{groupid}/users')
    routes.create_route(UsersApiKey, 'users/user/{userid}/apikey')
    routes.create_route(UsersApiKey, 'users/user/{userid}/apikey/{apikeyid}')
    routes.create_route(UsersApplication, 'users/user/{userid}/application/{appid}')
    routes.create_route(UsersGroup, 'users/user/{userid}/group/{groupid}')
    routes.create_route(UsersSearch, 'users/search/{search}')
    routes.create_route(User, 'users/user')
    routes.create_route(User, 'users/user/{userid}')
    routes.create_route(Users, 'users')
    routes.create_route(Authenticate, 'authenticate')
    # routes.create_route(Status, 'status')
    
    return routes


def main():
    parser = argparse.ArgumentParser(description='Start the eContext Classification Engine.')
    parser.add_argument("--config", dest="config_config_file", default="/etc/econtextauth/econtextauth.ini",
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

    route_objects = prepare_route_objects(config)
    app = get_app(
        config_get(config, 'econtextauth', 'access_log'),
        config_get(config, 'econtextauth', 'error_log'),
        middlewares=[Authenticator(route_objects['mapper'], route_objects['application_id'])]
    )
    routes = setup_routes(route_objects)
    setup_app(app, routes, route_prefix='api')

    server_config = dict(config.items('server'))
    options = {
        'worker_class': 'gevent',
        'bind': "{}:{}".format(server_config.get('host', '0.0.0.0'), server_config.get('port', '8000')),
        'workers': int(server_config.get('workers', cpu_count())),
        'threads': int(server_config.get('threads', 100)),
        'max_requests': server_config.get('max_requests', 1000),
        'graceful_timeout': server_config.get('graceful_timeout', 5),
        'pidfile': server_config.get('pidfile', '/tmp/econtextauth-engine.pid'),
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
