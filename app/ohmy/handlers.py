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

from .models import Ohmy




class NewOhmyHandler(UserHandler):
    
    @require_user
    def get(self):
        people_id = self.current_user.id
        oh = Ohmy()
        oh.start = datetime.now()
        oh.end = datetime.now()
        oh.people_id = people_id
        db.session.add(oh)
        db.session.commit()
        
        self.render('ohmy/create_oh.html', oh=oh)

    @require_user
    def post(self):
        people_id = self.current_user.id
        oh_id = self.get_argument('oh_id')
        oh = Ohmy.query.filter_by(id=oh_id).first_or_404()
        oh.end = datetime.now()
        delta = oh.end - oh.start
        oh.duration = delta.seconds
        db.session.add(oh)
        db.session.commit()
        return self.redirect('/ohmy')


class ShowOhShitlListHandler(UserHandler):
    @require_user
    def get(self):
        ohlist = Ohmy.query.filter_by(people_id=self.current_user.id).all()

        self.render('ohmy/show_oh_list.html', ohlist=ohlist)


app_handlers = [
    url('', ShowOhShitlListHandler, name='ohshit'),
    url('/new', NewOhShitHandler, name='new-ohshit'),
]



app_modules = {
   
}

app = DojangApp(
    'ohmy', __name__, handlers=app_handlers, ui_modules=app_modules,
)