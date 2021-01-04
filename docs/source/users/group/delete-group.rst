DELETE /users/user/{userid}/group/{groupid}
-------------------------------------------

Remove a Group from a User

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`users/user/{userid}/group/{groupid}`

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
      :api_url:`users/user/a3bc334a-f9f2-4797-aaa2-1440811c0ec0/group/16191e59-85e8-416f-826d-9cf8106c8cad`

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
