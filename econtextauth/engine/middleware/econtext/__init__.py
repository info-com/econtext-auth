import falcon
import traceback
import logging
import json

from falcon.http_error import NoRepresentation, HTTPError

log = logging.getLogger('econtext')


class eContextError(HTTPError):
    pass


def exception_handler(ex, req, resp, params):
    if isinstance(ex, falcon.HTTPError):
        "If the error is explicitly a falcon error, return it as is"
        raise ex

    status = falcon.HTTP_400
    title = str(ex)
    description = traceback.format_exc()
    raise eContextError(status, title, description)


def error_serializer(req, resp, exception):
    """
    Don't actually serialize the exception - just return the dictionary that we
    want.  The response body itself should be serialized in our middleware.

    @see econtext.engine.middleware.econtext.econtext
    """
    log.debug("error_serializer")
    resp.body = {"error": exception.to_dict()}
    log.debug(resp.body)
    if isinstance(exception, falcon.HTTPUnauthorized):
        resp.body = json.dumps(resp.body)
