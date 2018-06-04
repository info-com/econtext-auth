import falcon
import traceback
import logging
import json

from falcon.http_error import NoRepresentation, HTTPError

log = logging.getLogger('econtext')


class eContextError(HTTPError):
    pass


def error_serializer(req, resp, exception):
    """
    Don't actually serialize the exception - just return the dictionary that we
    want.  The response body itself should be serialized in our middleware.

    @see econtext.engine.middleware.econtext.econtext
    :type resp: falcon.Response
    
    """
    log.debug("error_serializer")
    resp.body = {"error": exception.to_dict()}
    log.debug(resp.body)
    if isinstance(exception, falcon.HTTPUnauthorized):
        resp.body = json.dumps(resp.body).encode("utf-8")
