GET /groups
-----------------

Retrieve a list of groups available in the system

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`groups`

Return
^^^^^^

A list of groups that exist in the eContext Auth API.

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`groups`

GET Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "groups": [
            {
              "status": "ENABLED",
              "application": "6CyMm9ikHh5ASSFOZ9OUWo",
              "href": ":api_url:`groups/group/4QlXPsKV1tis43vjTNwF7n`",
              "name": "api",
              "custom_data": {
                "classify_limit": 10,
                "tier_depth": 9
              },
              "created_at": "2017-04-12 21:46:02.264000+00:00",
              "modified_at": "2017-04-12 21:46:02.274000+00:00",
              "id": "4QlXPsKV1tis43vjTNwF7n",
              "description": "API user"
            },
            {
              "status": "ENABLED",
              "application": "6CyMm9ikHh5ASSFOZ9OUWo",
              "href": ":api_url:`groups/group/1OXxLiRU7Rv1tY8zqI8fxK`",
              "name": "api-free",
              "custom_data": {
                "classify_limit": 10
                "tier_depth": 9,
                "monthly_limit": 10000
              },
              "created_at": "2017-04-12 21:46:02.332000+00:00",
              "modified_at": "2017-04-12 21:46:02.343000+00:00",
              "id": "1OXxLiRU7Rv1tY8zqI8fxK",
              "description": "Free tier API users"
            },
            {
              "status": "ENABLED",
              "application": "6CyMm9ikHh5ASSFOZ9OUWo",
              "href": ":api_url:`groups/group/7Pmrb9Leujmf8gcspoRvje`",
              "name": "admin",
              "custom_data": {
                "company_id": 9999999,
                "_no_encrypt": true,
                "tier_depth": 9999
              },
              "created_at": "2017-04-12 21:46:02.301000+00:00",
              "modified_at": "2017-04-12 21:46:02.310000+00:00",
              "id": "7Pmrb9Leujmf8gcspoRvje",
              "description": "API admin users (typically admin or internal)"
            }
          ]
        },
        "elapsed": 0.03382992744445801
      }
    }
