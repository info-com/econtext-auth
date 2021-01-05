from .apikey import ApiKey
from .application import Application
from .application_parameter import ApplicationParameter
from .organization import Organization
from .data import Data
from .group import Group
from .user import User
from neomodel import db

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


def get_name():
    """
    Return the name of the mapper
    """
    return "neo4j"


def check_connection():
    """
    Run a simple query to see if the connection exists
    """
    result = False
    try:
        results, meta = db.cypher_query("Match () RETURN 1 LIMIT 1")
        result = True
    except:
        raise Exception("Could not connect to Neo4j")
    return result
