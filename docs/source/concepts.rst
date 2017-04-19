Concepts
========

Applications
------------

An Application is a concept which is used as the base resource against which Groups and
Users are checked against.  No Group or User may exist without a direct connection to an
Application.  An Application typically is comprised of an id, a name, and a description
but may also contain Custom Data.  When a User authenticates against the API the
credentials are checked against the specified Application.  Even if a username and
password happen to be correct, if a User is not associated with the application
specified in the authentication request, the request will fail.

The base Application inside the API is the "eContext Auth" Application which must be used
in order to access the API.

Groups
------

A Group provides associations and Custom Data inside an Application.  A particular group
may belong to a single Application and may be associated with many Users.

Users
-----

A User is an account which may be used to authenticate against the API.  A user may be
associated with many Applications and many Groups.  An authentication call against the
API must include the specific Application which a client is seeking access to.


Custom Data
-----------

Custom Data is an additional JSON field which is available in each of the above objects
and can be used to store additional information about a User, Group, or Application.