GET /applications/application/{appid}/users
-------------------------------------------

Retrieve a list of users currently associated with the Application identified by {appid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`applications/application/{appid}/users`

Return
^^^^^^

A list of Users associated with the Application.

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`applications/application/bf59fd16-d003-45ae-889d-4ed06b804c21/users`

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
                "bf59fd16-d003-45ae-889d-4ed06b804c21"
              ],
              "href": ":api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`",
              "groups": [],
              "apikeys": [],
              "id": "a3bc334a-f9f2-4797-aaa2-1440811c0ec0",
              "name": "Test User",
              "created_at": "2017-04-20 15:55:08.339000+00:00",
              "modified_at": "2017-04-20 15:55:08.377000+00:00",
              "custom_data": null,
              "email": "test-user@econtext.ai"
            }
          ]
        },
        "elapsed": 0.0032689571380615234
      }
    }
