# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import logging
import os
import time

from app.account.decorators import require_user, apiauth
from app.account.lib import SimpleApiHandler, CheckMixin
from app.account.models import People
from app.node.models import Node
from dojang.app import DojangApp
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict, create_token
from dojang.web import ApiHandler
from tornado import escape
from tornado.options import options
from tornado.web import UIModule
from tornado.web import URLSpec as url

from .lib import get_full_threads
from .models import Thread, ThreadNode


class ThreadTimelineHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        node_id = self.get_argument('node_id', None)
        count = self.get_argument('count', 20)
        page = self.get_argument('page', 1)

        node = ThreadNode.query.filter_by(id=node_id).first()
        if node is None:
            return self.render_json(result="404")

        pagination = Thread.query.filter_by(node_id=node.id).order_by("-id").paginate(page, count)
        pagination.items = get_full_threads(pagination.items)
        threads = []
        for thread in pagination.items:
            threads.append(thread.to_dict())

        return self.render_json(data=threads)


class ThreadNodeListHandler(SimpleApiHandler):
    def get(self):
      nodes = ThreadNode.query.all()
      node_list = []
      for node in nodes:
        node_list.append(node.to_dict())
      return self.render_json(data=node_list)


class NewThreadHandler(SimpleApiHandler):

    @apiauth
    def post(self):
       node_id = self.get_argument('node_id', None)
       people = self.current_user
       content = self.get_argument('content', None)
       now = datetime.now()
       node = ThreadNode.query.filter_by(id=node_id).first()
       if node is None:
           return self.render_json(result="404")

       thread = Thread()
       thread.people_id = people.id
       thread.node_id = node.id
       thread.content = content
       db.session.add(thread)
       db.session.commit()

       return self.render_json(result="200")


api_handlers = [
    #/v1/thread/timeline?node_name=xx
    url('/timeline', ThreadTimelineHandler),
    #/v1/thread/show?topic_id=xxx
    # url('/show', ShowTopicHandler),
    #/v1/thread/create?node_id=xxx&
    url('/new', NewThreadHandler),
    url('/node/list', ThreadNodeListHandler),

]

#api.xxx.com/v1/thread/(\d+)
app = DojangApp(
    'thread', __name__, version="v1", handlers=api_handlers
)
