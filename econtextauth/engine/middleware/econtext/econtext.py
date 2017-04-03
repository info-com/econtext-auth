"""
eContext middleware for Falcon which wraps the responses from the engine in a
top level eContext result object.  The result from a specific route has a JSON
attribute applied, and included in the whole object:

result = route_result.json
return {"econtext":{"result":result}}

"""
from __future__ import absolute_import

import json
import logging
from time import time

log = logging.getLogger('econtext')

class eContextJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.json
        except Exception:
            pass
        if isinstance(obj, (set, frozenset)):
            return list(obj)
        elif isinstance(obj, bytes):
            return {
                '__class__': 'bytes',
                '__value__': list(obj)
            }
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:
            pass

class EcontextMiddleware(object):
    def process_request(self, req, resp):
        """Process the request before routing it.
        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        pass

    def process_resource(self, req, resp, resource, params=None, *args, **kwargs):
        """Process the request after routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
        """
        try:
            req.context['body'] = json.loads(req.stream.read())
        except:
            pass
        if resource is not None:
            resource.start_time = time()
        return

    def process_response(self, req, resp, resource):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
        """
        if resource is None:
            return
        
        result = resp.body
        
        elapsed = time() - resource.start_time
        if hasattr(result, 'json'):
            result = result.json
        econtext_result = {u"result": result, u"elapsed": elapsed}
        
        ex = None
        if isinstance(result, dict):
            # This error would be set by the error_serializer
            # @see econtext.engine.middleware.econtext.error_serializer
            ex = result.get('error')
        if ex:
            del econtext_result['result']['error']
            log.debug("resp.status: {}".format(resp.status))
            econtext_result['status'] = resp.status
            econtext_result['error'] = ex['title']
            econtext_result['errorcode'] = resp.status.split(" ")[0]
            econtext_result['traceback'] = ex['description']
            #if isinstance(ex, falcon.HTTPError):
            #    resp.status = falcon.HTTP_BAD_REQUEST
            #    econtext_result['error'] = "{}: {}".format(ex.title, ex.description)
        
        resp.body = json.dumps({"econtext": econtext_result}, cls=eContextJsonEncoder)
        log.info("{} {} {}".format(req.method, resp.status, req.path))
