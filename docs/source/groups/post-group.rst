POST /groups/group
------------------

Create a new group object

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`groups/group`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "name", "string", "A name for the Group"
    "description", "string", "A description for the Group"
    "custom_data", "object", "A JSON object containing arbitrary data"
    "application", "string", "An Application ID"

Return
^^^^^^

A newly created Group Object

Example Request
^^^^^^^^^^^^^^^

POST Request
""""""""""""

.. parsed-literal::
    curl -X POST -u username:password \\
      -H 'content-type: application/json' \\
      -d '{
        "name": "Test Group",
        "description": "A test group",
        "custom_data": {
          "tier_depth": 9
        },
        "application": "bf59fd16-d003-45ae-889d-4ed06b804c21"
      }' \\
      :api_url:`groups/group`

POST Response
"""""""""""""

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
