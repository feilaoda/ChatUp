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

from .models import Ohmy

class GetOhShitListHandler(SimpleApiHandler):
    @apiauth
    def get(self):

        ohlist = Ohmy.query.filter_by(people_id=self.current_user.id).order_by('-id').all()
        ohlist_data = []
        for oh in ohlist:
            ohlist_data.append(oh.to_dict())
        return self.render_json(data=ohlist_data)


class NewOhShitHandler(SimpleApiHandler):
    @apiauth
    def post(self):
        oh = Ohmy()
        oh.start = self.get_argument('start', None)
        oh.end = self.get_argument('end', None)
        oh.people_id = self.current_user.id
        oh.duration = self.get_argument('duration', None)
        oh.day = self.get_argument('day', None)
        db.session.add(oh)
        db.session.commit()
        return self.render_json()

class EditOhShitHandler(SimpleApiHandler):
    @apiauth
    def post(self):
        oh_id = self.get_argument('id', None)
        if oh_id is None:
            oh = Ohmy.query.filter_by(id=oh_id).first_or_404()
        oh.start = self.get_argument('start', None)
        oh.end = self.get_argument('end', None)
        oh.people_id = self.current_user.id
        oh.duration = self.get_argument('duration', None)
        oh.day = self.get_argument('day', None)
        db.session.add(oh)
        db.session.commit()
        return self.render_json()

class DeleteOhShitHandler(SimpleApiHandler):
    @apiauth
    def post(self):
        oh_id = self.get_argument('id', None)
        if oh_id is None:
            oh = Ohmy.query.filter_by(id=oh_id).first_or_404()
        if oh.people_id != self.current_user.id:
            return self.send_error(403)

        db.session.delete(oh)
        db.session.commit()
        return self.render_json()

api_handlers = [
    url('/list.json', GetOhShitListHandler),
    url('/create.json', NewOhShitHandler),
    url('/update.json', EditOhShitHandler),
    url('/delete.json', DeleteOhShitHandler),
]

#api.iosplay.com/v1/wepusher/(\d+)
app = DojangApp(
    'ohshit', __name__, version="v1", handlers=api_handlers
)

