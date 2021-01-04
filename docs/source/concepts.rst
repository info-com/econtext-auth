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

Organizations
-------------

An Organization allows a structural hierarchy for storing Users. A User may not exist
alone outside of an organization. An Organization may also contain custom-data that will
then be associated with all of it's users.

Users
-----

A User is an account which may be used to authenticate against the API.  A user may be
associated with many Applications and many Groups but only with a single Organization.
An authentication call against the API must include the specific Application which a
client is seeking access to.

"Custom Data"
-------------

Additional data may be associated with Applications, Groups, and Users that may be used
downstream by Applications. For example, an Application may look for certain attributes
to be passed in with a User to override defaults, and those can be specified in the "Data"
or "Custom Data" attributes of a User.