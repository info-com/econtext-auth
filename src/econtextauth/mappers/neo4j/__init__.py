from .apikey import ApiKey
from .application import Application
from .application_parameter import ApplicationParameter
from .organization import Organization
from .data import Data
from .group import Group
from .user import User

"""
Indexes:

We assume that fulltext indexes have been created to enable search...

@see
https://neo4j.com/docs/cypher-manual/current/administration/indexes-for-full-text-search/


When we search for a user, we search:

* User.username
* User.email
* User.name
* ApiKey.key
* ApiKey.name
* ApiKey.description
* Application.name
* Application.description
* Group.name
* Group.description
* Organization.name

CALL db.index.fulltext.createNodeIndex(
    "broad_search_index",
    ["User", "Organization"],
    ["username", "email", "name", "description"],
    { analyzer: 'simple' }
)

CALL db.index.fulltext.queryNodes("broad_search_index", "econtext") YIELD node, score
RETURN node, score
"""