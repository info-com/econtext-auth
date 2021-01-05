Installation Instructions:
==========================

Generally the preferred method of install, currently, is to create a virtual environment and use pip to install.

```shell
$ python3 -m virtualenv econtext-auth
$ source econtext-auth/bin/activate
$ pip install git+ssh://git@github.com/info-com/econtext-auth
```

You may need to manually install gunicorn and gevent as they can sometimes be a little bit tricky.

This will install sources in the appropriate locations, including a configuration file in /etc/econtext/auth/ and an
executable in /usr/local/bin/econtextauth-engine.  You should have RethinkDB running locally, or change the
configuration file to point the appropriate location.

On a production machine, you should use init.d or system scripts to start and stop the server daemon on startup and
be able to control logging, etc.

There is a bug in remodel which is patched in my dev environment.  This bug prevents relations from being cleanly
removed.  The easy fix here is, once remodel is installed, to edit the remodel/models.py file and move line 113 down
below 116.


To run:
=======

```shell
$ sudo econtextauth-engine -vvv
```

Most robust logging, should tell you quite a bit.  Drop the "v" to reduce the logging more.
