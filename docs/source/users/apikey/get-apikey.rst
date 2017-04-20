GET /users/user/{userid}/apikey/{apikeyid}
------------------------------------------

Retrieve an existing API Key object for a User

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/user/{userid}/apikey/{apikeyid}`

Return
^^^^^^

An API Key object

Example Request
^^^^^^^^^^^^^^^

GET Request
"""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/apikey/44A62GBSEB4F3S08VFLWI0YCY`

GET Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "apikey": {
            "status": "ENABLED",
            "description": "An API Key for testing",
            "href": ":api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/apikey/44A62GBSEB4F3S08VFLWI0YCY`",
            "id": "44A62GBSEB4F3S08VFLWI0YCY",
            "name": "Test API Key"
          }
        },
        "elapsed": 0.06387519836425781
      }
    }
