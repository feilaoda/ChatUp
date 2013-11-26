# -*- coding: utf-8 -*-
import os
import hashlib
from datetime import datetime
import time
import logging
from tornado.web import UIModule 
from tornado.web import URLSpec as url
from tornado import escape
from tornado.options import options

from dojang.app import DojangApp
from dojang.util import ObjectDict, create_token
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.web import ApiHandler
from dojang.cache import cached, autocached, complex_cache, complex_cache_del

from app.account.lib import SimpleApiHandler, CheckMixin
from app.account.decorators import require_user, apiauth
from app.account.models import People

from app.node.models import Node
from .models import Topic, TopicReply
from .lib import get_full_topics, get_full_replies


class TopicTimelineHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        node_name = self.get_argument('node', None)
        order_by = self.get_argument('order_by', None)
        count = self.get_argument('count', 20)
        page = self.get_argument('page', 1)

        node = Node.query.filter_by(name=node_name).first()
        if node is None:
            return self.render_json(result="404")
        if order_by is None:
            order_by = node.sorting_by
        pagination = Topic.query.filter_by(node_id=node.id).order_by(order_by).paginate(page, count)
        pagination.items = get_full_topics(pagination.items)
        topics = []
        for topic in pagination.items:
            topics.append(topic.to_dict())

        return self.render_json(data=topics)

class ShowTopicHandler(SimpleApiHandler):
    @apiauth
    def get(self):
        topic_id = self.get_argument('topic_id',None)
        count = self.get_argument('count', 20)
        page = self.get_argument('page', 1)

        topic = Topic.query.filter_by(id=topic_id).first()
        if topic is None:
            return self.render_json(result="404")
        topic = get_full_topic(toipc)
        
        pagination = TopicReply.query.filter_by(topic_id=topic_id).order_by('-id').paginate(page, count)
        pagination.items = get_full_replies(pagination.items)
        res = dict()
        t = topic.to_dict()
        replies = []
        for reply in pagination.items:
            replies.append(reply.to_dict())
        t['replies'] = replies
        res['topic'] = t
        return self.render_json(data=res)

class ShowRepliesHandler(SimpleApiHandler):
    @apiauth
    def get(self):
        topic_id = self.get_argument('topic_id',None)
        count = self.get_argument('count', 20)
        page = self.get_argument('page', 1)

        topic = Topic.query.filter_by(id=topic_id).first()
        if topic is None:
            return self.render_json(result="404")
        
        pagination = TopicReply.query.filter_by(topic_id=topic_id).order_by('-id').paginate(page, count)
        pagination.items = get_full_replies(pagination.items)
        replies = []
        for reply in pagination.items:
            replies.append(reply.to_dict())
        return self.render_json(data=replies)
     
class NewTopicHandler(SimpleApiHandler):
    
    # @apiauth
    def post(self):
        node_name = self.get_argument('node_name', None)
        people = People.query.filter_by(username="admin").first()
        audio_url = None
        content = self.get_argument('content', None)
        # audio_duration = self.get_argument('duration', None)
        now = datetime.now()
        node = Node.query.filter_by(name=node_name).first()
        if node is None:
            return self.render_json(result="404")
        
        # if self.request.files:
        #     audio_file = self.request.files['audiofile'][0]
        #     if audio_file:
        #         token = str(int(time.time()))
        #         audio_name = "%d_%s.m4a" % (people.id, token)
        #         now_dir = now.strftime("%Y%m/%d")
        #         path_prefix = "/static/audio/topic/%s" % (now_dir)
        #         path_dir = options.local_media_path +path_prefix
        #         if not os.path.exists(path_dir):
        #             try:
        #                 os.makedirs(path_dir)
        #             except OSError as exc: # Python >2.5
        #                 if exc.errno == errno.EEXIST and os.path.isdir(path_dir):
        #                     logging.error(exc)

        #         dest_path = path_dir+"/"+audio_name
        #         audio_url = path_prefix+"/"+audio_name

        #         rawname = audio_file.get('filename')
        #         file_body = audio_file.get('body');
        #         try:
        #             write_file=open(dest_path,'wb+')
        #             write_file.write(file_body)
        #             write_file.close()
        #         except Exception, e:
        #             logging.error(e)
        #             return self.render_json(result="500")

        topic = Topic()
        topic.people_id = people.id
        topic.node_id = node.id
        topic.content = content
        # topic.media = audio_url
        # topic.media_duration = audio_duration

        db.session.add(topic)
        db.session.commit()

        return self.render_json(result="200")

class ReplyTopicHandler(SimpleApiHandler):
    @apiauth
    def post(self):
        node_id = self.get_argument('node_id', None)
        topic_id = self.get_argument('topic_id', None)
        people = self.current_user
        audio_url = None
        content = self.get_argument('content', None)
        # audio_duration = self.get_argument('duration', None)
        now = datetime.now()
        node = Node.query.filter_by(id=node_id).first()
        if node is None:
            return self.render_json(result="404")
        topic = Topic.query.filter_by(id=topic_id).first()
        if topic is None:
            return self.render_json(result="404")


        
        # if self.request.files:
        #     audio_file = self.request.files['audiofile'][0]
        #     if audio_file:
        #         token = str(int(time.time()))
        #         audio_name = "%d_%d_%s.m4a" % (topic.id, people.id, token)
        #         now_dir = now.strftime("%Y%m/%d")
        #         path_prefix = "/static/audio/%s" % (now_dir)
        #         path_dir = options.local_media_path +path_prefix
        #         if not os.path.exists(path_dir):
        #             try:
        #                 os.makedirs(path_dir)
        #             except OSError as exc: # Python >2.5
        #                 if exc.errno == errno.EEXIST and os.path.isdir(path_dir):
        #                     logging.error(exc)

        #         dest_path = path_dir+"/"+audio_name
        #         audio_url = path_prefix+"/"+audio_name

        #         rawname = audio_file.get('filename')
        #         file_body = audio_file.get('body');
        #         try:
        #             write_file=open(dest_path,'wb+')
        #             write_file.write(file_body)
        #             write_file.close()
        #         except Exception, e:
        #             logging.error(e)
        #             return self.render_json(result="500")

        reply = TopicReply()
        reply.people_id = self.current_user.id
        reply.topic_id = topic.id
        reply.content = content
        # reply.media = audio_url
        # reply.media_duration = audio_duration

        topic.reply_count += 1
        topic.last_reply_by = self.current_user.id
        topic.last_reply_time = now
        db.session.add(topic)
        db.session.add(reply)
        db.session.commit()


api_handlers = [
    #/v1/topic/timeline?node_name=xx
    url('/timeline', TopicTimelineHandler),
    #/v1/topic/show?topic_id=xxx
    url('/show', ShowTopicHandler),
    #/v1/topic/create?node_id=xxx&
    url('/create', NewTopicHandler),
    #/v1/topic/reply?topic_id=xxx&content=xxx
    url('/reply', ReplyTopicHandler),

    url('/show/replies', ShowRepliesHandler),
    
]

#api.keepcd.com/v1/topic/(\d+)
app = DojangApp(
    'topic', __name__, version="v1", handlers=api_handlers
)

