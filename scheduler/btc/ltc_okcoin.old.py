# -*- coding: utf-8 -*-
#!/usr/bin/env python

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

from gevent import monkey, queue
import gevent
import redis
import tornadoredis


monkey.patch_all()

#tc = tornadoredis.Client()
#tc.connect()
tc =  redis.Redis()



logger = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)

OKCOIN_URL = "https://www.okcoin.com/api/ticker.do?symbol=ltc_cny"

def create_request(url, headers=None):
    request = urllib2.Request(url)
    if headers:
        for k,v in headers.items():
            request.add_header(k, v)
    return request




class EasyWorker:
    def __init__(self, min_val, max_val):
        self.qin = queue.Queue(0)
        self.jobs = [gevent.spawn(self.do_fetch_data)]
        self.jobs += [gevent.spawn(self.do_alarmer)]
        self.job_count = len(self.jobs)
        self.headers = dict()
        self.headers['Accept'] = 'application/json;q=0.9,image/webp,*/*;q=0.8'
        self.min = min_val
        self.max = max_val
        self.alarming = False

    def start(self):
        gevent.joinall(self.jobs)




    def do_fetch_data(self):
        try:
            count = 0
            while True:
                #fetch data from okcoin
                try:
                    res = self.fetch_data(OKCOIN_URL)
                    if res['code'] == 200:
                        last = float(res['last'])
                        tc.publish('ltc:okcoin', last)
                        sleep(8)
                    else:
                        sleep(2)
                except Exception, e:
                    pass
                
                

                

        except Exception, e:
            logging.error("Scheduler Error!\n%s" % traceback.format_exc())
        finally:
            for i in range(self.job_count - 2):
                self.qin.put(StopIteration)
            self.job_count -= 1
            logging.debug("Scheduler done, job count: %s" % self.job_count)

    def fetch_data(self, url):
        logging.debug("Download starting...\n[%s]" % url)
        request = create_request(url, self.headers)
        try:
            response = urllib2.urlopen(request, timeout=10)
            html = response.read()
            if ('Content-Encoding' in response.headers and response.headers['Content-Encoding']) or \
                    ('content-encoding' in response.headers and response.headers['content-encoding']):
                    import gzip
                    import StringIO
                    data = StringIO.StringIO(html)
                    gz = gzip.GzipFile(fileobj=data)
                    html = gz.read()
                    gz.close()

            if 'Set-Cookie' in response.headers:
                cookies = response.headers['Set-Cookie']
                self.headers['Cookie'] = cookies

            response.close()
            logging.debug("Download end\n[%s]" % html)
            print html
            try:
                res = json.loads(html)
                low = res['ticker']['low']
                high = res['ticker']['high']
                last = res['ticker']['last']
                return dict(code=200, url=url, html=html, low=low, high=high, last=last)
            except Exception, e:
                logging.error("load error html json %s\n%s" % (html, traceback.format_exc()))
            

        except urllib2.HTTPError, e:
            logging.error('you got an error with the http code %s' % traceback.format_exc()) 
            return dict(code = e.code)
        except urllib2.URLError, e:
            logging.error('you got an error with the url code %s' % traceback.format_exc())
            return dict(code = 500)
        except Exception, e:
            logging.error('you got an unknow error: %s' % traceback.format_exc())
            return dict(code = 500)

        return dict(code=-1)


    def do_alarmer(self):
        try:
            item = self.qin.get()
            while item != StopIteration:
                try:
                    if item == "startalarm":
                        logging.debug( "get start")
                        
                        #self.start_alarm()
                    elif item == "stopalarm":
                        logging.debug( "get stop")
                        #self.stop_alarm()
                        
                except:
                    logging.error("Worker error!\n%s" % traceback.format_exc())
                item = self.qin.get()
        finally:
            self.job_count -= 1
            logging.debug("Worker done, job count: %s" % self.job_count)



if __name__ == "__main__":
    logger.debug("start ltc okcoin") 

    worker = EasyWorker(0, 0)
    worker.start()
    # res = worker.fetch_data('https://www.okcoin.com/api/ticker.do?symbol=ltc_cny')
    # print 'last = %s' % res['last']


