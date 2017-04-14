Installation Instructions:
==========================

Installation from source is currently the only method available.

```shell
$ git clone https://github.com/info-com/econtext-auth.git
$ cd econtext-auth/
$ sudo python2.7 setup.py install
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