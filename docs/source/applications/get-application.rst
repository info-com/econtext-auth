GET /applications/application/{appid}
-------------------------------------

Retrieve an existing application object identified by {appid}

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`applications/application/{appid}`

Return
^^^^^^

An Application object identified by {appid}

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`applications/application/bf59fd16-d003-45ae-889d-4ed06b804c21`

GET Response
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

