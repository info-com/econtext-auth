POST /applications/application
------------------------------

Create a new application object

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`applications/application`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "name", "string", "A name for the Application"
    "description", "string", "A description for the Application"
    "custom_data", "object", "A JSON object containing arbitrary data"

Return
^^^^^^

A newly created Application Object

Example Request
^^^^^^^^^^^^^^^

POST Request
""""""""""""

.. parsed-literal::
    curl -X POST -u username:password \\
      -H 'content-type: application/json' \\
      -d '{
        "name": "Test Application",
        "description": "Test application for use in this round of tests",
        "custom_data": {
          "spam": "and eggs"
        }
      }' \\
      :api_url:`applications/application`

POST Response
"""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "application": {
            "status": "ENABLED",
            "href": ":api_url:`applications/application/bf59fd16-d003-45ae-889d-4ed06b804c21`",
            "name": "Test Application",
            "custom_data": {
              "spam": "and eggs"
            },
            "created_at": "2017-04-19 19:51:14.409000+00:00",
            "modified_at": "2017-04-19 19:51:14.409000+00:00",
            "id": "bf59fd16-d003-45ae-889d-4ed06b804c21",
            "description": "Test application for use in this round of tests"
          }
        },
        "elapsed": 0.03231406211853027
      }
    }

