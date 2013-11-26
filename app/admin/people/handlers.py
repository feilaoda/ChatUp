# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

from tornado.web import UIModule, authenticated
from tornado.escape import utf8
from tornado.options import options
import tornado
from dojang.app import DojangApp
from dojang.cache import complex_cache
from dojang.database import db

from app.account.lib import UserHandler
from app.account.decorators import require_staff, require_admin, require_user, apiauth
from app.account.models import People


VOTE_UP = 1
VOTE_DOWN = 0

SAMPLE_PEOPLE=3


class AllPeoplesHandler(UserHandler):
    @require_admin
    def get(self): 
        p = self.get_argument('p', 1)
        peoples = People.query.filter_by().all()
        pagination = People.query.filter_by().order_by('id').paginate(p, 30)

        self.render('admin/people/all_peoples.html', pagination=pagination)

class ShowPeopleHandler(UserHandler):
    @require_admin
    def get(self, id): 
        people = People.query.filter_by(id=id).first_or_404()
        self.render('admin/people/show_people.html', people=people)

class EditPeopleHandler(UserHandler):
    @require_admin
    def get(self, id): 
        people = People.query.filter_by(id=id).first_or_404()
        self.render('admin/people/edit_people.html', people=people)

    @require_admin
    def post(self, id):
        description = self.get_argument('description', None)
        status = self.get_argument('status', None)
        description = description.strip()
        if description == "":
            description = None

        people = People.query.filter_by(id=id).first_or_404()
        if status == 'on':
            people.status = 1
        else:
            people.status = 0;
        people.description = description
        db.session.add(people)
        db.session.commit()

        self.redirect('/admin/people/%d' % people.id)



class DeleteTopicHandler(UserHandler):
    @require_admin
    def get(self): 
        peoples = People.query.filter_by.all()
        pagination = People.query.filter_by().order_by('id').paginate(p, 30)

        self.render('admin/people/show_peoples.html', pagination=pagination)



app_handlers = [
    ('', AllPeoplesHandler),
    ('/(\d+)', ShowPeopleHandler),
    ('/(\d+)/edit', EditPeopleHandler),
    ('/(\d+)/delete', DeleteTopicHandler),
]

app = DojangApp(
    'admin/people', __name__, handlers=app_handlers, 
)
