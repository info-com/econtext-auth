GET /applications
-----------------

Retrieve a list of applications available in the system

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`applications`

Return
^^^^^^

A list of applications that exist in the eContext Auth API.

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`applications`

GET Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "applications": [
            {
              "status": "ENABLED",
              "href": ":api_url:`applications/application/aa136fbd-26cc-448f-af0a-cf98fe165cc6`",
              "name": "eContext Auth",
              "custom_data": null,
              "created_at": "",
              "modified_at": "2017-04-14 16:38:05.025000+00:00",
              "id": "aa136fbd-26cc-448f-af0a-cf98fe165cc6",
              "description": "eContext Authentication/Authorization Application"
            }
          ]
        },
        "elapsed": 0.0014569759368896484
      }
    }
