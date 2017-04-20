Groups
======

A group is a resource that can be used to store various information about a group of users.  It can provide access to
common data in the custom_data field and can be used inside a client application to restrict access to resources based
on membership.  For example, in the eContext API, users in the "admin" group have access to more endpoints and have
encryption of eContext Category IDs turned off via the "_no_encrypt" flag found in the custom_data field of the "admin"
group.

A group may only belong to a single Application and must have a unique name inside that Application.  For example, there
may be multiple "admin" groups so long as they belong to different Application objects.  In a single Application, there
may only be a single group named "admin"

.. toctree::
    :maxdepth: 1

    get-groups
    post-group
    get-group
    put-group
    delete-group
    get-users