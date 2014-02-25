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
import cPickle
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
    app_res = []
    for name in coin_sets.keys():
        value = coin_sets[name]
        value = json.loads(value)
        coin_prices[name] = value
        summary += name + ": " +value['currency']+ str(value['last']) + "\n"
        #for ios app
        res = name + ":" + value['currency']+ str(value['last']) \
            + ", low:"+value['currency'] + str(value['low']) \
            + ", high:"+value['currency'] + str(value['high']) \
            + ", time:" + str(value['time'])
        app_res.append(res)

    data = dict()
    data['format'] = 'json'
    data['data'] = coin_prices

    #for web
    redis_client.set("web_"+BTC_CHANNEL, json.dumps(data))
    #for app
    redis_client.set("app_"+BTC_CHANNEL, cPickle.dumps("\n".join(app_res)))

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
    app_res = []
    for name in coin_sets.keys():
        value = coin_sets[name]
        value = json.loads(value)
        coin_prices[name] = value
        summary += name + ": " +value['currency']+ str(value['last']) + "\n"
        res = name + ":" + value['currency']+ str(value['last'])  \
            + ", low:"+value['currency'] + str(value['low']) \
            + ", high:"+value['currency'] + str(value['high']) \
            + ", time:" + str(value['time'])
        app_res.append(res)
    data = dict()
    data['format'] = 'json'
    data['data'] = coin_prices

    redis_client.set("web_"+LTC_CHANNEL, json.dumps(data))
    redis_client.set("app_"+LTC_CHANNEL, cPickle.dumps("\n".join(app_res)))

    ch = redis_client.hget(LIST_CHANNELS, LTC_CHANNEL)
    if ch is not None:
        ch = json.loads(ch)
        ch['summary'] = summary
        ch['update_at'] = nowstring
        print LTC_CHANNEL, "===>" , ch
        redis_client.hset(LIST_CHANNELS, LTC_CHANNEL, json.dumps(ch))



