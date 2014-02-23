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

from apscheduler.scheduler import Scheduler
from bitstamp import btc_worker as bitstamp_btc
from btc_e import btc_worker as btc_e_btc, ltc_worker as btc_e_ltc
from btcchina import btc_worker as btcchina_btc
from okcoin import btc_worker as okcoin_btc, ltc_worker as okcoin_ltc
from sync_job import sync_channel_btc, sync_channel_ltc


sched = Scheduler()
sched.start()

sched.add_cron_job(okcoin_btc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='*/10', max_instances=2)

sched.add_cron_job(okcoin_ltc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='*/10', max_instances=2)

sched.add_cron_job(btcchina_btc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='*/10', max_instances=2)

sched.add_cron_job(bitstamp_btc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='*/20', max_instances=1)

sched.add_cron_job(btc_e_btc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='0,20,40', max_instances=1)

sched.add_cron_job(btc_e_ltc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='10,30,50', max_instances=1)



#==============================================================================
#==============================================================================
#==============================================================================

sched.add_cron_job(sync_channel_btc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='*/10', max_instances=1)
 

sched.add_cron_job(sync_channel_ltc, 
    month="1-12", day='1-31',hour='0-23',minute='0-59', 
    second='*/10', max_instances=1)
 


while True:
    # print('This is the main thread.')
    time.sleep(2)

