PUT /groups/group/{groupid}
-------------------------------------

Update an existing group object identified by {groupid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`groups/group/{groupid}`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "name", "string", "A name for the Group"
    "description", "string", "A description for the Group"
    "custom_data", "object", "A JSON object containing arbitrary data"
    "status", "string", "The status of the Group.  Available options are ``ENABLED`` and ``DISABLED``"

Return
^^^^^^

An updated Group object

Example Request
^^^^^^^^^^^^^^^

PUT Request
"""""""""""

.. parsed-literal::
    curl -X PUT -u username:password \\
        -H 'content-type: application/json' \\
        -d '{
        "description": "A more detailed description of my group"
      }' \\
      :api_url:`groups/group/16191e59-85e8-416f-826d-9cf8106c8cad`

PUT Response
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
            "modified_at": "2017-04-20 15:40:10.116000+00:00",
            "id": "16191e59-85e8-416f-826d-9cf8106c8cad",
            "description": "A more detailed description of my group"
          }
        },
        "elapsed": 0.05748295783996582
      }
    }
