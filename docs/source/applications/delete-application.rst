DELETE /applications/application/{appid}
----------------------------------------

Delete the Application identified by {appid}.  An Application may not be deleted while there are users associated with
it.  You must first delete or remove the application association from any users before you will be able to delete the
Application.  This prevents orphaned User objects from being allowed to exist in the system.  Additionally, the
Application's status must be set to ``DISABLED``.

.. contents::
    :local:

Resource URL
^^^^^^^^^^^^
:api_url:`applications/application/{appid}`

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
      :api_url:`applications/application/bf59fd16-d003-45ae-889d-4ed06b804c21`

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

