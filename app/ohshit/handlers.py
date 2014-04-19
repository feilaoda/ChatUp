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
        oh_id = self.get_argument('id', None)
        if oh_id is None:
            people_id = self.current_user.id
            oh = Ohmy()
            oh.start = datetime.utcnow()
            oh.end = datetime.utcnow()
            oh.people_id = people_id
            oh.day = oh.start.strftime('%Y-%m-%d %H:%M:%S')
            db.session.add(oh)
            db.session.commit()
            return self.redirect('/ohshit/new?id=%d' % oh.id)
        else:
            oh = Ohmy.query.filter_by(id=oh_id).first_or_404()
            self.render('ohshit/create_oh.html', oh=oh)

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
        return self.redirect('/ohshit')

class DeleteOhmyHandler(UserHandler):
    @require_user
    def get(self, id):
        oh = Ohmy.query.filter_by(id=id).first()
        if oh:
            db.session.delete(oh)
            db.session.commit()
        return self.redirect('/ohshit')



class ShowOhmylListHandler(UserHandler):
    @require_user
    def get(self):
        ohlist = Ohmy.query.filter_by(people_id=self.current_user.id).order_by('-id').all()

        self.render('ohshit/show_oh_list.html', ohlist=ohlist)


app_handlers = [
    url('', ShowOhmylListHandler, name='ohshit'),
    url('/new', NewOhmyHandler, name='new-ohshit'),
    url('/delete/(\d+)', DeleteOhmyHandler, name='delete-ohshit'),
]



app_modules = {
   
}

app = DojangApp(
    'ohshit', __name__, handlers=app_handlers, ui_modules=app_modules,
)