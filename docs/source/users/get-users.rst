GET /users
----------

Retrieve a list of users available in the system.  This call is resource intensive and should generally be avoided in
favor or retrieving more targeted lists via search or application or group listings.

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users`

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
      :api_url:`users`

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
          ]
        },
        "elapsed": 0.004544973373413086
      }
    }
