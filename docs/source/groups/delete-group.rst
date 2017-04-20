DELETE /groups/group/{groupid}
----------------------------------------

Delete the Group identified by {groupid}.  The Group's status must be set to ``DISABLED`` before deletion is possible.

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`groups/group/{groupid}`

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
      :api_url:`groups/group/16191e59-85e8-416f-826d-9cf8106c8cad`

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

