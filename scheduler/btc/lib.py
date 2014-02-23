# -*- coding: utf-8 -*-
#!/usr/bin/env python

import StringIO
from datetime import datetime
import gzip
import json
import logging
import os
import sys
import sys
import threading
from time import sleep
import time
import traceback
import urllib2
import wave


def create_request(url, headers=None):
    request = urllib2.Request(url)
    if headers:
        for k,v in headers.items():
            request.add_header(k, v)
    return request

def fetch_html(url, headers):
        logging.debug("Download starting...\n[%s]" % url)
        request = create_request(url, headers)
        try:
            response = urllib2.urlopen(request, timeout=10)
            html = response.read()
            if ('Content-Encoding' in response.headers and response.headers['Content-Encoding']) or \
                    ('content-encoding' in response.headers and response.headers['content-encoding']):
                    
                    data = StringIO.StringIO(html)
                    gz = gzip.GzipFile(fileobj=data)
                    html = gz.read()
                    gz.close()

            if 'Set-Cookie' in response.headers:
                cookies = response.headers['Set-Cookie']
                headers['Cookie'] = cookies

            response.close()
            logging.debug("Download end\n[%s]" % html)
            try:
                res = json.loads(html)
                return dict(code=200, url=url, html=res)
            except Exception, e:
                logging.error("load error html json %s\n%s" % (html, traceback.format_exc()))

        except urllib2.HTTPError, e:
            logging.error('you got an error with the http code %s' % traceback.format_exc()) 
            return dict(code = e.code, url=url)
        except urllib2.URLError, e:
            logging.error('you got an error with the url code %s' % traceback.format_exc())
            return dict(code = 500, url=url)
        except Exception, e:
            logging.error('you got an unknow error: %s' % traceback.format_exc())
            return dict(code = 500, url=url)
        return dict(code=-1)

