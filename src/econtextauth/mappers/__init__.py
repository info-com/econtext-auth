"""
All mapper classes should provide a method to retrieve a standard Model
from the neomodel class. The standard Model should be generic enough that
it should be relatively easy to drop in another mapper without having
to rebuild the entire app.

For example to update a user, maybe it should look like this:

    >>> user = mapper.User.get(user_id).to_object()
    >>> user.set_name("Some New Name")
    >>> mapper.User.save(user)

Any mapper needs to implement the interface
"""

