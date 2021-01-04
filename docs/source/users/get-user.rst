GET /users/user/{userid}
------------------------

Retrieve an existing User object identified by {userid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/user/{userid}`

Return
^^^^^^

A User object identified by {userid}

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`

GET Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "user": {
            "username": "test-user@econtext.ai",
            "status": "UNVERIFIED",
            "applications": [
              {
                "status": "ENABLED",
                "href": "https://auth.econtext.ai/api/applications/application/609543d6-1cca-4039-9c1a-c843bda15ba4",
                "name": "Test Application",
                "custom_data": null,
                "created_at": "2017-05-08 19:21:13.381000+00:00",
                "modified_at": "2017-05-08 19:21:13.381000+00:00",
                "id": "609543d6-1cca-4039-9c1a-c843bda15ba4",
                "description": "Test application for use in this round of tests"
              }
            ],
            "href": ":api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`",
            "groups": [],
            "apikeys": [],
            "id": "a3bc334a-f9f2-4797-aaa2-1440811c0ec0",
            "name": "Test User",
            "created_at": "2017-04-20 15:55:08.339000+00:00",
            "modified_at": "2017-04-20 15:55:08.339000+00:00",
            "custom_data": null,
            "email": "test-user@econtext.ai"
          }
        },
        "elapsed": 0.0007190704345703125
      }
    }
