import rethinkdb as rethinkdb
from gevent import monkey; monkey.patch_all()
import falcon
import gunicorn.app.base
import argparse
from os.path import abspath
from econtextauth.engine import routes
from econtextauth.engine.middleware.econtext.econtext import EcontextMiddleware
from econtextauth.engine.middleware.econtext import exception_handler, error_serializer
from multiprocessing import cpu_count

import remodel.connection
import rethinkdb as r

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import logging
log = logging.getLogger('econtext')

# Here's our app!
app = falcon.API(middleware=[EcontextMiddleware()])
app.add_error_handler(Exception, exception_handler)
app.set_error_serializer(error_serializer)


################################################################################
# Base settings (where to find files)
################################################################################
settings = {
    'rethinkdb_host': 'localhost'
}


################################################################################
# Define our Gunicorn Application
################################################################################

class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """
    A standalone Gunicorn application that can be started directly in Python
    without using the gunicorn command line options.
    """
    
    def __init__(self, application, options=None):
        self.options = dict(options or {})
        self.application = application
        super(StandaloneApplication, self).__init__()
    
    def load_config(self):
        tmp_config = map(
            lambda item: (item[0].lower(), item[1]),
            self.options.iteritems()
        )
        
        config = dict(
            (key, value)
            for key, value in tmp_config
            if key in self.cfg.settings and value is not None
        )
        
        for key, value in config.iteritems():
            self.cfg.set(key.lower(), value)
    
    def load(self):
        return self.application


def get_log_level(v=0):
    if v is None or v == 0:
        return logging.ERROR
    elif v > 2:
        return logging.DEBUG
    elif v > 1:
        return logging.INFO
    elif v > 0:
        return logging.WARNING


def get_log(v):
    log_level = get_log_level(v)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(asctime)s] [%(process)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"))
    log.addHandler(h)
    h.setLevel(log_level)
    log.setLevel(log_level)


def setup_app(config):
    if config is None:
        econtext_config = settings
        get_log(2)
    else:
        econtext_config = dict(config.items('econtextauth'))

    rethinkdb_host = econtext_config.get('rethinkdb_host')
    rethinkdb_port = econtext_config.get('rethinkdb_port', 28015)
    log.debug("Loading RethinkDB from {}:{}".format(rethinkdb_host, rethinkdb_port))
    #rethinkdb = r.connect(rethinkdb_host, rethinkdb_port, db='econtext_users')
    remodel.connection.pool.configure(host=rethinkdb_host, port=rethinkdb_port, db="econtext_users")
    
    route_options = {
        'rethinkdb': rethinkdb,
    }
    
    for route_class in routes.route_classes:
        if hasattr(route_class, 'routes'):
            for route in route_class.routes:
                log.info("Loading route: /api/{}".format(route))
                app.add_route("/api/{}".format(route), route_class.get_route_constructor(route_options))


def main():
    parser = argparse.ArgumentParser(description='Start the eContext Classification Engine.')
    parser.add_argument("--config", dest="config_config_file", default="/etc/econtext/auth/econtextauth.ini", help="Configuration file", metavar="PATH")
    parser.add_argument("-v", dest="config_verbose", action="count", default=0, help="Be more or less verbose")
    options = parser.parse_args()
    get_log(options.config_verbose)
    
    config = configparser.ConfigParser()
    if options.config_config_file is not None:
        log.debug("Loading configuration file from %s", abspath(options.config_config_file))
        config_file = open(abspath(options.config_config_file))
        config.readfp(config_file)
    
    del options.config_config_file
    del options.config_verbose
    
    for k,v in options.__dict__.items():
        if v is not None:
            section, key = k.split("_", 1)
            log.debug("Overriding configuration: {} {} = {}".format(section, key, v))
            config.set(section, key, str(v))
    
    setup_app(config)
    server_config = dict(config.items('server'))
    
    options = {
        'worker_class': 'gevent',
        'bind': "{}:{}".format(server_config.get('host', '0.0.0.0'), server_config.get('port', '8000')),
        'workers': int(server_config.get('workers', cpu_count())),
        'threads': int(server_config.get('threads', 100)),
        'max_requests': server_config.get('max_requests', 100000),
        'graceful_timeout': server_config.get('graceful_timeout', 5),
        'pidfile': server_config.get('pidfile', '/var/run/econtext-auth-engine.pid'),
        'preload_app': True,
        
        # CALLBACKS
        #'post_fork': post_fork,
        #'worker_exit': worker_exit,
        #'post_request': post_request,
        #'pre_request': pre_request,
        #'worker_abort': worker_oops
    }
    try:
        StandaloneApplication(app, options).run()
    except Exception:
        log.exception("Caught an Exception...")


if __name__ == '__main__':
    main()