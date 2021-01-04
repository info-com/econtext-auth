GET /users/search/{search}
--------------------------

Retrieve a list of users available in the system that match the provided search term.  This method performs a case-
insensitive "contains" search against a User's email, name, id, API Keys, and a company name (inside custom_data) if it
exists.

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/search/{search}`

Return
^^^^^^

A list of Users

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`users/search/econtext.ai`

GET Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "users": [
            {
              "username": "test-user@econtext.ai",
              "status": "UNVERIFIED",
              "applications": [],
              "href": ":api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`",
              "groups": [
                {
                  "status": "ENABLED",
                  "application": "609543d6-1cca-4039-9c1a-c843bda15ba4",
                  "href": "https://auth.econtext.ai/api/groups/group/5fb6f5d6-3a6d-4e1d-83bb-7445274745bf",
                  "name": "Test Group",
                  "custom_data": {
                    "tier_depth": 9
                  },
                  "created_at": "2017-05-08 19:22:48.867000+00:00",
                  "modified_at": "2017-05-08 19:22:48.871000+00:00",
                  "id": "5fb6f5d6-3a6d-4e1d-83bb-7445274745bf",
                  "description": "A test group with some custom_data"
                }
              ],
              "apikeys": [],
              "id": "a3bc334a-f9f2-4797-aaa2-1440811c0ec0",
              "name": "Test User",
              "created_at": "2017-04-20 15:55:08.339000+00:00",
              "modified_at": "2017-04-20 19:46:25.426000+00:00",
              "custom_data": null,
              "email": "test-user@econtext.ai"
            }
          ]
        },
        "elapsed": 0.011507034301757812
      }
    }
