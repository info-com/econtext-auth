POST /users/user
----------------

Create a new User object

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/user`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "email", "string", "A valid email address"
    "password", "string", "A password for the User - must be at least 7 characters long"
    "name", "string", "A name for the User"
    "custom_data", "object", "A JSON object containing arbitrary data"
    "applications", "array", "A list of Application object IDs"
    "groups", "array", "A list of Group object IDs"

Return
^^^^^^

A newly created User object

Example Request
^^^^^^^^^^^^^^^

POST Request
""""""""""""

.. parsed-literal::
    curl -X POST \
      -H 'authorization: Basic b3BzQGluZm8uY29tOnAxdjBwcjBzMW0=' \\
      -H 'cache-control: no-cache' \\
      -H 'content-type: application/json' \\
      -d '{
        "name":"Test User",
        "email":"test-user@econtext.ai",
        "password":"a new password",
        "applications":["ec48dad3-ca61-4d74-a584-3ee3db4708ef"]
      }' \\
      :api_url:`users/user`

POST Response
"""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "user": {
            "username": "test-user@econtext.ai",
            "status": "UNVERIFIED",
            "applications": [
              "ec48dad3-ca61-4d74-a584-3ee3db4708ef"
            ],
            "href": "api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`",
            "groups": [
              "16191e59-85e8-416f-826d-9cf8106c8cad"
            ],
            "apikeys": [],
            "id": "a3bc334a-f9f2-4797-aaa2-1440811c0ec0",
            "name": "Test User",
            "created_at": "2017-04-20 15:55:08.339000+00:00",
            "modified_at": "2017-04-20 15:55:08.339000+00:00",
            "custom_data": null,
            "email": "test-user@econtext.ai"
          }
        },
        "elapsed": 0.0005970001220703125
      }
    }
