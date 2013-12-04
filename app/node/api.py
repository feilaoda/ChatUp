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


from app.account.lib import SimpleApiHandler, CheckMixin
from app.account.decorators import require_user, apiauth
from app.account.models import People
from app.util import find_mention

from .models import LanguageChannel,LanguageResource, LanguageTopic, LanguageTopicComment
from .models import ChannelSubscribe, StudyRecord

class NewTopicHandler(SimpleApiHandler):

    @apiauth
    def post(self, node_id):
        people_id = 1

        content = self.get_argument('content', None)
        duration = self.get_argument('duration', None)
        now = datetime.now()

        token = str(int(time.time()))
        audio_name = "%d_%s.m4a" % (people_id, token)
        now_dir = now.strftime("%Y%m/%d")
        path_prefix = "/static/audio/%s" % (now_dir)
        path_dir = options.local_media_path +path_prefix
        if not os.path.exists(path_dir):
            try:
                os.makedirs(path_dir)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path_dir):
                    logging.error(exc)

        dest_path = path_dir+"/"+audio_name
        audio_url = path_prefix+"/"+audio_name
        if self.request.files:
            audio_file = self.request.files['audiofile'][0]
            if audio_file:
                rawname = audio_file.get('filename')
                file_body = audio_file.get('body');
                try:
                    write_file=open(dest_path,'wb+')
                    write_file.write(file_body)
                    write_file.close()
                except Exception, e:
                    logging.error(e)
                    return self.render_json(result="500")

        topic = LanguageTopic()
        topic.people_id = self.current_user.id
        topic.node_id = node_id
        topic.audio = audio_url
        topic.audio_duration = duration
        topic.content = content
        db.session.add(topic)
        db.session.commit()

        return self.render_json(result="200")

class ShowNodeHandler(SimpleApiHandler):
    @apiauth
    def get(self, node_id):
        node = Node.query.filter_by(id=node_id).first()
        if node is None:
            return self.render_json(result="404")
        
        page = self.get_argument('page', 1)
        count = self.get_argument('count', 20)
        toipcs = Topic.query.filter_by('node_id'=node.id).order_by(node.sorting_by).limit(count).all()
        for topic in topics:
            topic = get_full_topic(topics)
        
        topics_array = []
        for topic in topics:
            topics_array.append(topic.to_dict())
        node_dict = dict()
        node_dict = node.to_dict()
        node_dict['topics'] = topics_array
        return self.render_json(data=node_dict)





api_handlers = [
    url('/(\d+)/new', NewTopicHandler),
    url('/(\d+)', ShowNodeHandler)
]

#api.keepcd.com/v1/topic/(\d+)
app = DojangApp(
    'node', __name__, version="v1", handlers=api_handlers
)

