PUT /applications/application/{appid}
-------------------------------------

Update an existing application object identified by {appid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`applications/application/{appid}`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "name", "string", "A name for the Application"
    "description", "string", "A description for the Application"
    "custom_data", "object", "A JSON object containing arbitrary data"
    "status", "string", "The status of the Application.  Available options are ``ENABLED`` and ``DISABLED``"

Return
^^^^^^

An updated Application Object

Example Request
^^^^^^^^^^^^^^^

PUT Request
"""""""""""

.. parsed-literal::
    curl -X PUT -u username:password \\
        -H 'content-type: application/json' \\
        -d '{
        "custom_data": {
          "green eggs": "and ham"
        }
      }' \\
      :api_url:`applications/application/bf59fd16-d003-45ae-889d-4ed06b804c21`

PUT Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "application": {
            "status": "ENABLED",
            "href": ":api_url:`applications/application/bf59fd16-d003-45ae-889d-4ed06b804c21`",
            "name": "Test Application",
            "custom_data": {
              "green eggs": "and ham"
            },
            "created_at": "2017-04-19 19:51:14.409000+00:00",
            "modified_at": "2017-04-19 19:52:16.618000+00:00",
            "id": "bf59fd16-d003-45ae-889d-4ed06b804c21",
            "description": "Test application for use in this round of tests"
          }
        },
        "elapsed": 0.01231406211853027
      }
    }

