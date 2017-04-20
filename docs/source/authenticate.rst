Authentication
==============

The main purpose of the eContext Auth API is to allow a user to authenticate against an Application defined in
the system.

POST /authenticate
------------------

Authenticate a user against an application resource.

Resource URL
^^^^^^^^^^^^
:api_url:`authenticate`

Parameters
^^^^^^^^^^

.. csv-table::
    :header: "Parameter","Type","Description"
    :stub-columns: 1
    :widths: 25, 20, 100

    "type", "string", "What type of authentication to perform.  Currently it must be either ``username`` or ``apikey``"
    "application", "string", "The id of the application to authenticate to"
    "credential", "object", "The username and password to authenticate with"
    "credential.username", "string", "The username to authenticate with (or the apikey.id)"
    "credential.password", "string", "The password to authenticate with (or the apikey.secret)"

Return
^^^^^^

The authenticate call typically returns a ``true`` or ``false`` value to indicate whether the credentials are valid.

Example Request
^^^^^^^^^^^^^^^

POST Request
""""""""""""

.. parsed-literal::
    curl -X POST  -u username:password \\
      -H 'content-type: application/json' \\
      -d '{
        "type": "username",
        "credential": {
          "username": USERNAME,
          "password": PASSWORD
        },
        "application": APP_ID
      }'
      :api_url:`authenticate`

POST Response
"""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "authenticated": true
        },
        "elapsed": 0.0038661956787109375
      }
    }
