# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib
import json

from app.account.decorators import require_user, require_admin
from app.account.lib import UserHandler, SimpleApiHandler
from app.account.models import People
from dojang.app import DojangApp
from dojang.cache import complex_cache
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import create_token
from tornado.escape import utf8
from tornado.options import options
from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url

from .models import PushGroup, PushText, PushChannel


class RecentPushTextHandler(UserHandler):
    
    @require_user
    def get(self):
      

        btc_set = complex_cache.hgetall('btc_price')
        print btc_set
        btc_prices = dict()
        for price in btc_set:
            btc_prices[price] = json.loads(btc_set[price])

        ltc_set = complex_cache.hgetall('ltc_price')
        print ltc_set
        ltc_prices = dict()
        for price in ltc_set:
            ltc_prices[price] = json.loads(ltc_set[price])


        texts = PushText.query.filter_by(people_id=people_id, sync=0).all()
        
        self.render('wepusher/recent_push.html', texts=texts, btc_prices=btc_prices, ltc_prices=ltc_prices)



class NewPushTextHandler(UserHandler):
    
    @require_user
    def get(self):
        people_id = self.current_user.id
        
        self.render('wepusher/create_push.html')

    @require_user
    def post(self):
        people_id = self.current_user.id
        content = self.get_argument('pushtext')
        text = PushText()
        text.people_id = people_id
        text.content = content
        text.sync = 0
        text.create_at = datetime.utcnow()
        db.session.add(text)
        db.session.commit()
        return self.redirect('/wepusher')



#==============================Channel==============================
#==============================Channel==============================
#==============================Channel==============================



class NewPushChannelHandler(UserHandler):
    
    @require_user
    def get(self):
        people_id = self.current_user.id
        
        self.render('wepusher/create_channel.html')

    @require_user
    def post(self):
        people_id = self.current_user.id
        name = self.get_argument('name')
        title = self.get_argument('title')
        description = self.get_argument('description')
        channel = PushChannel()
        channel.people_id = people_id
        channel.name = name
        channel.title = title
        channel.description = description
        channel.permission = 0;
        channel.token = create_token(32)
        channel.create_at = datetime.utcnow()
        db.session.add(channel)
        db.session.commit()
        return self.redirect('/wepusher/channel')



class ShowChannelHandler(UserHandler):
    
    def get(self, channel_id):
        people_id = self.current_user.id
        channel = PushChannel.query.filter_by(id=channel_id).first_or_404()

        channel_data = complex_cache.get("detail_"+channel.name)

        if(channel_data is not None):
            channel_data = json.loads(channel_data)
            if(channel_data['format'] == 'json'):
                data = channel_data['data']
                return self.render('wepusher/show_channel_template.html', channel=channel, data=data)

        btc_set = complex_cache.hgetall(channel.name)
        print btc_set
        btc_prices = dict()
        for price in btc_set:
            btc_prices[price] = json.loads(btc_set[price])

        self.render('wepusher/show_channel.html', channel=channel, btc_prices=btc_prices
            )



class ShowChannelListHandler(UserHandler):
    @require_user
    def get(self):
        HSET_CHANNELS = "lst:channels"
        chs = complex_cache.hgetall(HSET_CHANNELS)
        people_id = self.current_user.id
        channels = []
        print chs
        if chs is None or len(chs)==0:
            chs = PushChannel.query.filter_by(people_id=people_id).all()
            for ch in chs:
                channel = dict()
                channel['id'] = ch.id
                channel['name'] = ch.name
                channel['title'] = ch.title
                channel['summary'] = ''
                channel['update_at'] = ''
                channels.append(channel)
                complex_cache.hset(HSET_CHANNELS, ch.name, json.dumps(channel))
        else:
            for k in chs.keys():
                v = chs[k]
                v = json.loads(v)
                print "v", v
                channels.append(v)

        self.render('wepusher/show_channel_list.html', channels=channels)


#==============================Group==============================
#==============================Group==============================
#==============================Group==============================


class NewPushGroupHandler(UserHandler):
    
    @require_admin
    def get(self):
        people_id = self.current_user.id
        
        self.render('wepusher/create_group.html')

    @require_admin
    def post(self):
        people_id = self.current_user.id
        title = self.get_argument('title')
        description = self.get_argument('description')
        group = PushGroup()
        group.title = title
        group.description = description
        group.create_at = datetime.utcnow()
        db.session.add(group)
        db.session.commit()
        return self.redirect('/wepusher/group')



class ShowGroupHandler(UserHandler):
    
    def get(self, group_id):
        people_id = self.current_user.id
        group = PushGroup.query.filter_by(id=group_id).first_or_404()
        channels = PushChannel.query.filter_by(group_id=group_id).all()

        self.render('wepusher/show_group.html', channels=channels)


class ShowGroupListHandler(UserHandler):
    def get(self):
        groups = PushGroup.query.filter_by().all()

        self.render('wepusher/show_group_list.html', groups=groups)


class SyncPushTextHandler(SimpleApiHandler):
    
    def get(self, people_id):

        texts = PushText.query.filter_by(people_id=people_id, sync=0).all()
        
        self.render('wepusher/recent_groups.html', groups=groups)

class ShowChannelHandler(UserHandler):
    
    def get(self, channel_id):
        people_id = self.current_user.id
        channel = PushChannel.query.filter_by(id=channel_id).first_or_404()

        channel_data = complex_cache.get("detail_"+channel.name)

        if(channel_data is not None):
            channel_data = json.loads(channel_data)
            if(channel_data['format'] == 'json'):
                data = channel_data['data']
                return self.render('wepusher/show_channel_template.html', channel=channel, data=data)

        btc_set = complex_cache.hgetall(channel.name)
        print btc_set
        btc_prices = dict()
        for price in btc_set:
            btc_prices[price] = json.loads(btc_set[price])

        self.render('wepusher/show_channel.html', channel=channel, btc_prices=btc_prices
            )


"""
hset: key, field, value
key:btc_charts
field:btc/okcoin
value:{price: 100.0, time:2014}

"""

app_handlers = [
    url('', ShowGroupListHandler, name='push'),
    url('/new', NewPushTextHandler, name='new-push'),
    url('/group', ShowGroupListHandler, name='list-push-group'),
    url('/group/new', NewPushGroupHandler, name='new-push-group'),
    url('/group/(\d+)', ShowGroupHandler, name='show-push-group'),
    url('/channel', ShowChannelListHandler, name='list-push-channel'),
    url('/channel/new', NewPushChannelHandler, name='new-push-channel'),
    url('/channel/(\d+)', ShowChannelHandler, name='show-push-channel'),
]


class PushChannelTemplateModule(UIModule):    
    def render(self, channel, data):
        return self.render_string('wepusher/channel/%s.html' % channel.name, data=data)

 

app_modules = {
    "PushChannelTemplate": PushChannelTemplateModule
}



app = DojangApp(
    'wepusher', __name__, handlers=app_handlers, ui_modules=app_modules,
)