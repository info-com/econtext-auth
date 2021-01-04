PUT /users/user/{userid}/apikey/{apikeyid}
------------------------------------------

Update an API Key object.  An API Key which has a status of ``DISABLED`` may not be used to authenticate a User.

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`/users/user/{userid}/apikey/{apikeyid}`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "name", "string", "A name for the API Key"
    "description", "string", "A description for the API Key"
    "status", "string", "The status of the API Key.  Available options are ``ENABLED`` and ``DISABLED``"

Return
^^^^^^

An API Key object

Example Request
^^^^^^^^^^^^^^^

PUT Request
"""""""""""

.. parsed-literal::
    curl -X POST \\
      -H 'authorization: Basic b3BzQGluZm8uY29tOnAxdjBwcjBzMW0=' \\
      -H 'cache-control: no-cache' \\
      -H 'content-type: application/json' \\
      -d '{
        "status":"DISABLED"
      }' \\
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/apikey/44A62GBSEB4F3S08VFLWI0YCY`

PUT Response
""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "apikey": {
            "status": "DISABLED",
            "description": "An API Key for testing",
            "secret": "ODBkZjZiNzYtMzU1Ny00MDgxLWFiMDYtMWE1OGU5OTIxZGQ0",
            "href": ":api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/apikey/44A62GBSEB4F3S08VFLWI0YCY`",
            "id": "44A62GBSEB4F3S08VFLWI0YCY",
            "name": "Test API Key"
          }
        },
        "elapsed": 0.029818058013916016
      }
    }
