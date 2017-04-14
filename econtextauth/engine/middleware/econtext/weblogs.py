# -*- encoding: utf-8 -*-

import logging
import logging.handlers
import os
import basicauth
import datetime
from dateutil.tz import tzlocal

log = logging.getLogger('econtext')


class WebLogs(object):
    def __init__(self, conf):
        self.access_log_path = os.path.abspath(conf.get('access_log'))
        self.error_log_path = os.path.abspath(conf.get('error_log'))
        self.access_log = None
        self.error_log = None
        if self.access_log_path:
            log.info("Sending access log events to {}".format(self.access_log_path))
            self.access_log = logging.getLogger('weblogs.access')
            handler = logging.handlers.WatchedFileHandler(self.access_log_path)
            self.access_log.addHandler(handler)
            self.access_log.setLevel(logging.INFO)
        if self.error_log_path:
            log.info("Sending error log events to {}".format(self.error_log_path))
            self.error_log = logging.getLogger('weblogs.error')
            handler = logging.handlers.WatchedFileHandler(self.error_log_path)
            formatter = logging.Formatter("ERROR: %(asctime)s\n * PROCESS ID: %(process)d\n * THREAD ID: %(thread)d\n%(message)s")
            handler.setFormatter(formatter)
            self.error_log.addHandler(handler)
            self.error_log.setLevel(logging.INFO)
    
    def process_response(self, req, resp, resource):
        """
        Log events
        
        :param req:
        :param resp:
        :param resource:
        :return:
        """
        try:
            log.debug("weblogs.process_response")
            if self.access_log:
                self.access_log.info(self.build_access_line(req, resp))
            if self.error_log and resp.context.get('exception'):
                self.error_log.error(resp.context.get('exception').description)
        except Exception as e:
            pass
    
    def build_access_line(self, req, resp):
        """
        Standard combined web log format:
        {remote_addr} - {remote_user} [{time_local}] "{request}" {status} {body_bytes_sent} "{http_referer}" "{http_user_agent}"
    
        :type req: falcon.Request
        :type resp: falcon.Response
        :param req:
        :param resp:
        :return:
        """
        return " ".join((
            str(req.access_route[-1]),
            str('-'),
            str(self.get_username(req)),
            str(datetime.datetime.now(tz=tzlocal()).strftime('[%d/%b/%Y:%H:%M:%S %z]')),
            str(self.get_request(req)),
            str(resp.status.split(" ")[0]),
            str(len(resp.body)),
            '"{}"'.format(req.env.get("HTTP_REFERER", '-')),
            '"{}"'.format(req.user_agent or '-')
        ))
    
    def get_request(self, req):
        """
        :type req: falcon.Request
        :param req:
        """
        return '"{} {} {}"'.format(req.method, req.relative_uri, req.env.get('SERVER_PROTOCOL'))
    
    def get_username(self, req):
        try:
            username, password = basicauth.decode(req.auth)
            return username
        except:
            pass
        return '-'

