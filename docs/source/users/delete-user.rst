DELETE /users/user/{userid}
---------------------------

Delete the User identified by {userid}.  The User's status must be set to ``DISABLED`` before deletion is possible.

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/user/{userid}`

Return
^^^^^^

A boolean response explaining whether the ``DELETE`` call was successful or not.

Example Request
^^^^^^^^^^^^^^^

DELETE Request
""""""""""""""

.. parsed-literal::
    curl -X DELETE -u username:password \\
      -H 'content-type: application/json' \\
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0`

DELETE Response
"""""""""""""""

.. parsed-literal::
    {
      "econtext": {
        "result": {
          "deleted": true
        },
        "elapsed": 0.0257871150970459
      }
    }

