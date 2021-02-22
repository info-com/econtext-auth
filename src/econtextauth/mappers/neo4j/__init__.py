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
    { analyzer: 'standard-no-stop-words' }
)

# Some analyzers
# CALL db.index.fulltext.listAvailableAnalyzers
simple
standard-no-stop-words
unicode_whitespace

CALL db.index.fulltext.queryNodes("broad_search_index", "econtext") YIELD node, score
RETURN node, score
"""

CREATE_INDEX_CYPHER = """CALL db.index.fulltext.createNodeIndex(
    "broad_search_index",
    ["User", "Organization"],
    ["username", "email", "name", "description"],
    { analyzer: 'standard-no-stop-words' }
)
"""
CHECK_INDEX_QUERY = """CALL db.indexes() YIELD name WHERE name="broad_search_index" RETURN name"""


def get_name():
    """
    Return the name of the mapper
    """
    return "neo4j"


def check_connection() -> bool:
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


def check_indexes() -> bool:
    """
    Checks (and potentially installs) search indexes
    """
    result = False
    try:
        results, meta = db.cypher_query(CHECK_INDEX_QUERY)
        if not results:
            results, meta = db.cypher_query(CREATE_INDEX_CYPHER)
        result = True
    except:
        raise Exeption("Unable to verify search indexes...manually create and try again")
    return result
