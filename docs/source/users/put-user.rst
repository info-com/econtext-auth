PUT /users/user/{userid}
------------------------

Update an existing User object identified by {userid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/user/{userid}`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "email", "string", "A valid email address"
    "password", "string", "A password for the User - must be at least 7 characters long"
    "name", "string", "A name for the User"
    "custom_data", "object", "A JSON object containing arbitrary data"
    "applications", "array", "A list of Application object IDs"
    "groups", "array", "A list of Group object IDs"
    "status", "string", "The status of the User.  Available options are ``ENABLED``, ``UNVERIFIED``, and ``DISABLED``"

Return
^^^^^^

An updated User object

Example Request
^^^^^^^^^^^^^^^

PUT Request
"""""""""""

.. parsed-literal::
    curl -X PUT -u username:password \\
        -H 'content-type: application/json' \\
        -d '{
        "status": "ENABLED"
        "groups": ["16191e59-85e8-416f-826d-9cf8106c8cad"]
      }' \\
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`

PUT Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "user": {
            "username": "test-user@econtext.ai",
            "status": "ENABLED",
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
            "modified_at": "2017-04-20 16:00:37.922000+00:00",
            "custom_data": null,
            "email": "test-user@econtext.ai"
          }
        },
        "elapsed": 0.0007190704345703125
      }
    }
