GET /groups/group/{groupid}
-------------------------------------

Retrieve an existing group object identified by {groupid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`groups/group/{appid}`

Return
^^^^^^

A Group object identified by {groupid}

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`groups/group/16191e59-85e8-416f-826d-9cf8106c8cad`

GET Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "group": {
            "status": "ENABLED",
            "application": "bf59fd16-d003-45ae-889d-4ed06b804c21",
            "href": ":api_url:`groups/group/16191e59-85e8-416f-826d-9cf8106c8cad`",
            "name": "Test Group",
            "custom_data": {
              "tier_depth": 9
            },
            "created_at": "2017-04-20 15:37:46.092000+00:00",
            "modified_at": "2017-04-20 15:37:46.116000+00:00",
            "id": "16191e59-85e8-416f-826d-9cf8106c8cad",
            "description": "A test group"
          }
        },
        "elapsed": 0.05748295783996582
      }
    }
