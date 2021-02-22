Installation Instructions:
==========================

Generally the preferred method of install, currently, is to create a virtual environment and use pip to install.

```shell
$ python3 -m virtualenv econtext-auth
$ source econtext-auth/bin/activate
$ pip install git+ssh://git@github.com/info-com/econtext-auth
$ neomodel_install_labels econtextauth.mappers.neo4j --db bolt://neo4j:neo4j@localhost:7687
```

The last line here installs indexes and constraints for the object models.
@see https://neomodel.readthedocs.io/en/latest/getting_started.html#applying-constraints-and-indexes

You may need to manually install gunicorn and gevent as they can sometimes be a little bit tricky.

This will install sources in the appropriate locations, including a configuration file in /etc/econtext/auth/ and an
executable in /usr/local/bin/econtextauth-engine.  You should have RethinkDB running locally, or change the
configuration file to point the appropriate location.

On a production machine, you should use init.d or system scripts to start and stop the server daemon on startup and
be able to control logging, etc.

There is a bug in remodel which is patched in my dev environment.  This bug prevents relations from being cleanly
removed.  The easy fix here is, once remodel is installed, to edit the remodel/models.py file and move line 113 down
below 116.

You can install to systemd using the provided econtextauth.service unit file:

```shell
$ sudo su -
$ cp /path/to/econtextauth.service /etc/systemd/system/econtextauth.service
$ chmod -r 0644 /var/log/econtextauth
$ systemctl enable econtextauth.service
```


To run:
=======

```shell
$ sudo econtextauth-engine -vvv
```

Most robust logging, should tell you quite a bit.  Drop the "v" to reduce the logging more.

If you've installed using systemd, then run the following to start:

```shell
$ sudo systemctl start econtextauth.service
```

