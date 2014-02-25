# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import logging
import os
import time
import json

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

from .models import PushGroup, PushChannel


class GetGroupListHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        groups = PushGroup.query.filter_by().all()

        group_list = []
        for group in groups:
            group_list.append(group.to_dict())
        return self.render_json(data=group_list)

class GetChannelListHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        group_id = self.get_argument('group_id')
        channels = PushChannel.query.filter_by(group_id=group_id).all()

        channel_list = []
        for ch in channels:
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

class GetChannelHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        channel_id = self.get_argument('channel_id')
        channel = PushChannel.query.filter_by(id=channel_id).first_or_404()
        channel.summary = ""
        channel_data = complex_cache.get("app_"+channel.name)
        print channel_data
        if channel_data is not None:

            channel_json_data = json.loads(channel_data)
            # if(channel_json_data['format'] == 'json'):
                # data = channel_json_data['data']
            channel.summary = channel_json_data
            channel.format = 'json'

        channel_texts = []
        channel_texts.append(channel.to_dict())
        return self.render_json(data=channel_texts)


api_handlers = [
    #/v1/topic/timeline?node_name=xx
    url('/group_list.json', GetGroupListHandler),
    url('/group.json', GetChannelListHandler),
    url('/channel_list.json', GetChannelListHandler),
    url('/channel.json', GetChannelHandler),
]

#api.iosplay.com/v1/wepusher/(\d+)
app = DojangApp(
    'wepusher', __name__, version="v1", handlers=api_handlers
)

