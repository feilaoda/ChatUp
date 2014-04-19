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
import wave

from lib import fetch_html
import redis
from keynames import BTC_ORIG_CHANNEL, LTC_ORIG_CHANNEL


redis_client =  redis.Redis()

def save_ticker(key, ticker):
    
    field = "btc-e"
    value = json.dumps(ticker)
    redis_client.hset(key, field, value)

def fetch_ticker(key, url):
    
    headers = dict()
    headers['Accept'] = 'application/json;q=0.9,image/webp,*/*;q=0.8'
    now = time.localtime()
    timestring  = time.strftime("%Y-%m-%d %H:%M:%S", now)
    res = fetch_html(url, headers)
    if res['code'] == 200:
        ticker = res['html']['ticker']
        if ticker.has_key('last'):
            last = float(ticker['last'])
        
        newticker = dict()
        newticker['time'] = timestring
        newticker['bid'] = ticker['buy']
        newticker['ask'] = ticker['sell']
        newticker['vol'] = ticker['vol_cur']
        newticker['high'] = ticker['high']
        # newticker['updated'] = ticker['updated']
        newticker['low'] = ticker['low']
        newticker['last'] = ticker['last']
        newticker['currency'] = "$"
        save_ticker(key, newticker)
        print newticker
    else:
        print res


def btc_worker():
    # print "fetch ltc from okcoin job"
    url = "https://btc-e.com/api/2/btc_usd/ticker"
    fetch_ticker(BTC_ORIG_CHANNEL, url)
    
def ltc_worker():
    # print "fetch ltc from okcoin job"
    url = "https://btc-e.com/api/2/ltc_usd/ticker"
    fetch_ticker(LTC_ORIG_CHANNEL, url)
    




