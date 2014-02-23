# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib

from app.account.decorators import require_user, require_admin
from app.account.lib import UserHandler, SimpleApiHandler
from app.account.models import People
from app.channel.models import Channel, ChannelEntry
from app.group.models import Group
from app.topic.models import Topic
from dojang.app import DojangApp
from dojang.cache import cached
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict
from tornado.escape import utf8
from tornado.options import options
from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url


class ShowRecentChannelsHandler(UserHandler):
    @require_admin
    def get(self):
        channels = Channel.query.filter_by().all()
        self.render('admin/channel/all_channels.html', channels=channels)



class ShowChannelHandler(UserHandler):
    @require_admin
    def get(self, id):
        channel = Channel.query.filter_by(id=id).first_or_404()
        entries = channel.entries
        for entry in entries:
            if channel.isa == "topic":
                topic = Topic.query.filter_by(id=entry.entry_id).first()
                entry.topic = topic
         
        self.render('admin/channel/show_channel_%s.html' % channel.isa, channel=channel, entries=entries)
            


class NewChannelHandler(UserHandler):
    @require_admin
    def get(self):
        channel = Channel()
        self.render('admin/channel/create_channel.html', channel=channel)

    @authenticated
    def post(self):
        channel = Channel()
        title = self.get_argument('title', None)
        isa = self.get_argument('isa', None)
        pic = self.get_argument('pic', None)
        channel.title = title
        channel.isa = isa
        channel.sorting = 0
        db.session.add(channel)
        db.session.commit()
        self.redirect('/admin/channel/%d' % channel.id)


class EditChannelHandler(UserHandler):
    @require_admin
    def get(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first_or_404()
        self.render('admin/channel/edit_channel.html', channel=channel)

    @authenticated
    def post(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first_or_404()
        title = self.get_argument('title', None)
        isa = self.get_argument('isa', None)
        channel.title = title
        channel.isa = isa
        channel.sorting = 0
        db.session.add(channel)
        db.session.commit()
        self.redirect('/admin/channel/%d' % channel.id)



class NewChannelEntryHandler(UserHandler):
    @require_admin
    def get(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first_or_404()
        channel_entity = ChannelEntry()
        self.render('admin/channel/create_channel_entry.html', channel=channel, channel_entry=channel_entity)

    def create_or_edit(self, channel, entry):
        entry_id = self.get_argument('entry_id', None)
        url = self.get_argument('url', None)
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        pic = self.get_argument('pic', None)

        
        if entry is None:
            entry = ChannelEntry()
            entry.entry_id = entry_id
            entry.channel_id = channel.id

        if channel.isa == "topic":
            print "channel is topic"
            topic = Topic.query.filter_by(id=entry_id).first_or_404()
            if url is None or url == "":
                print "channel url is None"
                entry.url = "/topic/%d" % topic.id
            else:
                entry.url = url
            if title is None or title == "":
                print "channel title is None"
                entry.title = topic.title
            else:
                entry.title = title
            entry.content = content
            entry.pic = pic

        entry.sorting = 0
        db.session.add(entry)
        db.session.commit()
        self.redirect('/admin/channel/%d' % channel.id)

    @require_admin
    def post(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first_or_404()

        self.create_or_edit(channel, None)

class EditChannelEntryHandler(NewChannelEntryHandler):
    @require_admin
    def get(self, channel_id, channel_entry_id):
        channel = Channel.query.filter_by(id=channel_id).first_or_404()
        entry = ChannelEntry.query.filter_by(id=channel_entry_id).first_or_404()
        self.render('admin/channel/edit_channel_entry.html', channel=channel, channel_entry=entry)

    @require_admin
    def post(self, channel_id, channel_entry_id):
        channel = Channel.query.filter_by(id=channel_id).first_or_404()
        entry = ChannelEntry.query.filter_by(id=channel_entry_id).first()

        self.create_or_edit(channel, entry)



class DeleteChannelEntryHandler(UserHandler):
    @require_admin
    def get(self, channel_id, channel_entity_id):
        channel = Channel.query.filter_by(id=channel_id).first_or_404()
        channel_entity = ChannelEntry.query.filter_by(id=channel_entity_id).first_or_404()
        db.session.delete(channel_entity)
        db.session.commit()

        self.redirect('/admin/channel/%d' % channel.id)


class SortChannelEntryHandler(SimpleApiHandler):
    @require_admin
    def post(self, channel_id):
        ids = self.get_arguments('ids[]', [])
        entities = []
        for id in ids:
            entity = ChannelEntry.query.filter_by(id=id, channel_id=channel_id).first()
            if entity:
                entities.append(entity)

        if len(entities) > 0:            
            index = 1
            for entity in entities:
                if entity.sorting != index:
                    entity.sorting = index
                    db.session.add(entity)
                index += 1
            db.session.commit()
        
        return self.render_json({'result':'ok', 'array': ids})
        

app_handlers = [
    url('', ShowRecentChannelsHandler, name='admin-all-channels'),
    url('/new', NewChannelHandler, name='admin-new-channel'),
    url('/(\d+)/edit', EditChannelHandler, name='admin-edit-channel'),    
    url('/(\d+)', ShowChannelHandler, name='admin-show-channel'),

    url('/(\d+)/new', NewChannelEntryHandler, name='admin-new-channel-entity'),
    url('/(\d+)/sort', SortChannelEntryHandler, name='admin-sort-channel-entity'),
    url('/(\d+)/(\d+)/edit', EditChannelEntryHandler, name='admin-edit-channel-entity'),
    url('/(\d+)/(\d+)/delete', DeleteChannelEntryHandler, name='admin-delete-channel-entity'),

    # url('/sort', SortBoardHandler, name='admin-sort-channel'),
]


class ChannelFormModule(UIModule):
    def render(self, channel):        
        return self.render_string('admin/channel/channel_form.html', channel=channel)

class ChannelEntryFormModule(UIModule):
    def render(self, channel, channel_entry):        
        return self.render_string('admin/channel/channel_entry_form.html', channel=channel, channel_entry=channel_entry)



app_modules = {
    'ChannelForm': ChannelFormModule,
    'ChannelEntryForm':ChannelEntryFormModule
}



app = DojangApp(
    'admin/channel', __name__, handlers=app_handlers, ui_modules=app_modules,
)


