GET /groups/group/{groupid}/users
-------------------------------------------

Retrieve a list of users currently associated with the Group identified by {groupid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`groups/group/{groupid}/users`

Return
^^^^^^

A list of Users associated with the Group.

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`groups/group/16191e59-85e8-416f-826d-9cf8106c8cad/users`

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
                "ec48dad3-ca61-4d74-a584-3ee3db4708ef"
              ],
              "href": ":api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`",
              "groups": [
                "16191e59-85e8-416f-826d-9cf8106c8cad"
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
