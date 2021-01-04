DELETE /users/user/{userid}/application/{appid}
-----------------------------------------------

Remove an Application from a User.  Please note that a User must be associated with at least one Application.  Removing
the last Application from a User will result in a 409 Conflict error.

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/user/{userid}/application/{appid}`

Return
^^^^^^

A boolean response explaining whether the ``DELETE`` call was successful or not.

Example Request
^^^^^^^^^^^^^^^

DELETE Request
""""""""""""""

.. parsed-literal::
    curl -X GET -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/application/aa136fbd-26cc-448f-af0a-cf98fe165cc6`

DELETE Response
"""""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "deleted": true
        },
        "elapsed": 0.030797958374023438
      }
    }
