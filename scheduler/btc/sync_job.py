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

from keynames import BTC_CHANNEL, LTC_CHANNEL
from keynames import BTC_ORIG_CHANNEL, LTC_ORIG_CHANNEL
# from keynames import BTC_WEB_CHANNEL, LTC_WEB_CHANNEL
# from keynames import BTC_APP_CHANNEL, LTC_APP_CHANNEL

from keynames import GROUP_CHANNELS, GROUP_CHANNELS_WEB, GROUP_CHANNELS_APP

redis_client =  redis.Redis()



 


def sync_channel_btc():
    now = time.localtime()
    nowstring  = time.strftime("%Y-%m-%d %H:%M:%S", now)

    coin_sets= redis_client.hgetall(BTC_ORIG_CHANNEL)
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

    web_data = dict()
    web_data['format'] = 'json'
    web_data['data'] = coin_prices

    #for web
    # redis_client.set(BTC_WEB_CHANNEL, json.dumps(web_data))
    #for app
    # redis_client.set(BTC_APP_CHANNEL, cPickle.dumps("\n".join(app_res)))

    # redis_client.hset(GROUP_CHANNELS_WEB, BTC_CHANNEL, json.dumps(data))
    # redis_client.hset(GROUP_CHANNELS_APP, BTC_CHANNEL, cPickle.dumps("\n".join(app_res)))
    ch = dict()
    ch['name'] = 'ltc'
    ch['update_at'] = nowstring
    ch['summary'] = app_res
    redis_client.hset(GROUP_CHANNELS_APP, BTC_CHANNEL, cPickle.dumps(ch))

    ch['summary'] = web_data
    redis_client.hset(GROUP_CHANNELS_WEB, BTC_CHANNEL, cPickle.dumps(ch))

    ch['summary'] = summary
    print BTC_CHANNEL, "===>" , ch
    redis_client.hset(GROUP_CHANNELS, BTC_CHANNEL, cPickle.dumps(ch))

def sync_channel_ltc():
    now = time.localtime()
    nowstring  = time.strftime("%Y-%m-%d %H:%M:%S", now)

    coin_sets= redis_client.hgetall(LTC_ORIG_CHANNEL)
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
    web_data = dict()
    web_data['format'] = 'json'
    web_data['data'] = coin_prices

    # redis_client.set(LTC_WEB_CHANNEL, json.dumps(web_data))
    # redis_client.set(LTC_APP_CHANNEL, cPickle.dumps("\n".join(app_res)))
    
    ch = dict()
    ch['name'] = 'ltc'
    ch['update_at'] = nowstring
    ch['summary'] = app_res
    redis_client.hset(GROUP_CHANNELS_APP, LTC_CHANNEL, cPickle.dumps(ch))
    
    ch['summary'] = web_data
    redis_client.hset(GROUP_CHANNELS_WEB, LTC_CHANNEL, cPickle.dumps(ch))

    ch['summary'] = summary
    print LTC_CHANNEL, "===>" , ch
    redis_client.hset(GROUP_CHANNELS, LTC_CHANNEL, cPickle.dumps(ch))



