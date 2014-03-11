# -*- coding: utf-8 -*-
#!/usr/bin/env python
import json
import time

from lib import fetch_html
import redis
from keynames import BTC_ORIG_CHANNEL


redis_client =  redis.Redis()


def save_ticker(key, ticker):
    
    field = "btcchina"
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
        newticker = dict()
        newticker['bid'] = ticker['buy']
        newticker['ask'] = ticker['sell']
        newticker['vol'] = ticker['vol']
        newticker['time'] = timestring
        newticker['high'] = ticker['high']
        newticker['low'] = ticker['low']
        newticker['last'] = ticker['last']
        newticker['currency'] = "¥"
        save_ticker(key, newticker)
        print newticker
    else:
        print res


def btc_worker():
    url = "https://data.btcchina.com/data/ticker"
    fetch_ticker(BTC_ORIG_CHANNEL, url)




    