POST /users/user/{userid}/apikey
--------------------------------

Create a new API Key object for a User

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`/users/user/{userid}/apikey`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "name", "string", "A name for the API Key"
    "description", "string", "A description for the API Key"

Return
^^^^^^

A newly created API Key object including the generated secret.  The secret is only returned as a result of the POST
call.  Subsequent calls to retrieve this key will not return the secret, and it is hashed in the database.  Please be
sure to pass the secret back to the user for safe storage.

Example Request
^^^^^^^^^^^^^^^

POST Request
""""""""""""

.. parsed-literal::
    curl -X POST \\
      -H 'authorization: Basic b3BzQGluZm8uY29tOnAxdjBwcjBzMW0=' \\
      -H 'cache-control: no-cache' \\
      -H 'content-type: application/json' \\
      -d '{
        "name":"Test API Key",
        "description":"An API Key for testing"
      }' \\
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/apikey`

POST Response
"""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "apikey": {
            "status": "ENABLED",
            "description": "An API Key for testing",
            "secret": "ODBkZjZiNzYtMzU1Ny00MDgxLWFiMDYtMWE1OGU5OTIxZGQ0",
            "href": ":api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/apikey/44A62GBSEB4F3S08VFLWI0YCY`",
            "id": "44A62GBSEB4F3S08VFLWI0YCY",
            "name": "Test API Key"
          }
        },
        "elapsed": 0.06387519836425781
      }
    }
