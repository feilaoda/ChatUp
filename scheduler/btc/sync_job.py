# -*- coding: utf-8 -*-
#!/usr/bin/env python

from datetime import datetime
import json
import logging
import os
import sys
import sys
from time import sleep
import time
import traceback
import urllib2

import redis


redis_client =  redis.Redis()

LTC_CHANNEL = "ltc_price"
BTC_CHANNEL = "btc_price"
LIST_CHANNELS = "lst:channels"

def sync_channel_btc():
    now = time.localtime()
    nowstring  = time.strftime("%Y-%m-%d %H:%M:%S", now)

    coin_sets= redis_client.hgetall(BTC_CHANNEL)
    coin_prices = dict()
    summary = ""
    for name in coin_sets.keys():
        value = coin_sets[name]
        value = json.loads(value)
        coin_prices[name] = value
        summary += name + ": " +value['currency']+ str(value['last']) + "\n"
    data = dict()
    data['format'] = 'json'
    data['data'] = coin_prices

    redis_client.set("detail_"+BTC_CHANNEL, json.dumps(data))

    ch = redis_client.hget(LIST_CHANNELS, BTC_CHANNEL)
    if ch is not None:
        ch = json.loads(ch)
        ch['summary'] = summary
        ch['update_at'] = nowstring
        print BTC_CHANNEL, "===>" , ch
        redis_client.hset(LIST_CHANNELS, BTC_CHANNEL, json.dumps(ch))

def sync_channel_ltc():
    now = time.localtime()
    nowstring  = time.strftime("%Y-%m-%d %H:%M:%S", now)

    coin_sets= redis_client.hgetall(LTC_CHANNEL)
    coin_prices = dict()
    summary = ""
    for name in coin_sets.keys():
        value = coin_sets[name]
        value = json.loads(value)
        coin_prices[name] = value
        summary += name + ": " +value['currency']+ str(value['last']) + "\n"
    data = dict()
    data['format'] = 'json'
    data['data'] = coin_prices

    redis_client.set("detail_"+LTC_CHANNEL, json.dumps(data))

    ch = redis_client.hget(LIST_CHANNELS, LTC_CHANNEL)
    if ch is not None:
        ch = json.loads(ch)
        ch['summary'] = summary
        ch['update_at'] = nowstring
        print LTC_CHANNEL, "===>" , ch
        redis_client.hset(LIST_CHANNELS, LTC_CHANNEL, json.dumps(ch))



