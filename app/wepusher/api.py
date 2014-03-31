# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import logging
import os
import time
import json
import cPickle

from app.account.decorators import require_user, apiauth
from app.account.lib import SimpleApiHandler, CheckMixin
from app.account.models import People
from app.node.models import Node
from dojang.app import DojangApp
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict, create_token
from dojang.web import ApiHandler
from dojang.cache import complex_cache

from tornado import escape
from tornado.options import options
from tornado.web import UIModule
from tornado.web import URLSpec as url

from .models import PushGroup, PushChannel, PushText
from keynames import *

BTC_ORIG_CHANNEL = "wp.ch.orig.btc"
LTC_ORIG_CHANNEL = "wp.ch.orig.ltc"

BTC_CHANNEL = "btc"
LTC_CHANNEL = "ltc"

GROUP_CHANNELS = "wp.group.ch"
GROUP_CHANNELS_WEB = "wp.group.ch.web"
GROUP_CHANNELS_APP = "wp.group.ch.app"

class GetGroupListHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        groups = PushGroup.query.filter_by().all()

        group_list = []
        for group in groups:
            group_list.append(group.to_dict())
        return self.render_json(data=group_list)

class GetGroupHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        group_id = self.get_argument('group_id')
        channels = PushChannel.query.filter_by(group_id=group_id).all()

        channel_list = []
        for ch in channels:
            channel_data = complex_cache.hget(GROUP_CHANNELS, ch.name)
            if channel_data is not None:
                # print channel_data
                channel_cache_data = cPickle.loads(channel_data)
                # print channel_cache_data
                ch.summary = channel_cache_data['summary']
            channel_list.append(ch.to_dict())
        return self.render_json(data=channel_list)



# class GetChannelListHandler(GetGroupHandler):
#     pass

    # # @apiauth
    # def get(self):
    #     group_id = self.get_argument('group_id')
    #     channels = PushChannel.query.filter_by(group_id=group_id).all()

    #     channel_list = []
    #     for ch in channels:
    #         channel_list.append(ch.to_dict())
    #     return self.render_json(data=channel_list)


GROUP_CHANNELS_APP = "wp.group.ch.app"

class GetChannelHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        channel_id = self.get_argument('channel_id')
        channel = PushChannel.query.filter_by(id=channel_id).first_or_404()
        channel.summary = ""
        channel_data = complex_cache.hget(GROUP_CHANNELS_APP, channel.name)
        if channel_data is not None:
            channel_cache_data = cPickle.loads(channel_data)
            # if(channel_json_data['format'] == 'json'):
                # data = channel_json_data['data']
            channel.summary = "\n".join(channel_cache_data['summary'])
            channel.format = 'text'

        channel_texts = []
        channel_texts.append(channel.to_dict())
        return self.render_json(data=channel_texts)


class PostPushTextHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        user = self.get_argument('key', None)
        if user is None:
            return self.send_error(404)
        people = People.query.filter_by(token=user).first_or_404()
        title = self.get_argument('title', '')
        message = self.get_argument('message', None)
        device = self.get_argument('device', None)
        # if message is None or message == '':
        #     return self.send_error(404)

        text = PushText()
        text.people_id = people.id
        text.title = title
        text.message = message
        # text.device = device
        db.session.add(text)
        db.session.commit()

        return self.render_json()


api_handlers = [
    #/v1/topic/timeline?node_name=xx
    url('/group_list.json', GetGroupListHandler),
    url('/group.json', GetGroupHandler),
    url('/channel_list.json', GetGroupHandler),
    url('/channel.json', GetChannelHandler),
    url('/push.json', PostPushTextHandler),

]

#api.iosplay.com/v1/wepusher/(\d+)
app = DojangApp(
    'wepusher', __name__, version="v1", handlers=api_handlers
)

#api.wepusher.com/v1/push.json
wepusher_app = DojangApp(
    '', __name__, version="v1", handlers=api_handlers
)
