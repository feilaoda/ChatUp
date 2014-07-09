# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib
from tornado.escape import utf8
from tornado.options import options
from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url


from dojang.app import DojangApp
from dojang.cache import autocached
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict

from app.account.decorators import require_user
from app.account.lib import UserHandler
from app.account.models import People
from app.wist.models import Wist, WistContent, WistStar



class PeopleAllWistsHandler(UserHandler):

    def get(self, username):
        people = People.query.filter_by(username=username).first_or_404()

        p = self.get_argument('p', 1)
        limit = 30
        pagination = Wist.query.filter_by(people_id=people.id).order_by('-id').paginate(p, limit)

        self.render('people/show_people_wists.html', people=people, pagination=pagination)



class ShowPeopleWistHandler(UserHandler):
    def get(self, username, wist_id):
        people = People.query.filter_by(username=username).first_or_404()
        wist = Wist.query.filter_by(id=wist_id).first_or_404()
        fork_count = wist.fork_count
        if wist.fork_root_id != 0:
            forked_root_wist = Wist.query.filter_by(id=wist.fork_root_id).first()
            if forked_root_wist:
                fork_count = forked_root_wist.fork_count
        if wist.content:
            wist_content = wist.content
        else:
            wist_content = WistContent()

        return self.render('wist/show_wist.html', wist=wist, content=wist_content, fork_count=fork_count)

class ShowPeopleStarsWistHandler(UserHandler):
    def get(self, username):
        p = self.get_argument('p', 1)
        limit = 30

        people = People.query.filter_by(username=username).first_or_404()
        pagination = WistStar.query.filter_by(people_id=people.id).paginate(p, limit)
        wist_list = []
        for star in pagination.items:
            wist = star.wist
            #wist = Wist.query.filter_by(id=star.wist_id).first()
            if wist:
                wist_list.append(wist)
        pagination.items = wist_list

        return self.render('wist/star_list.html', pagination=pagination)





app_handlers = [
    url('/(\w+)/wist', PeopleAllWistsHandler, name='show-people-all-wists'),
    url('/(\w+)/wist/stars', ShowPeopleStarsWistHandler, name='show-people-starred-wist'),  
    url('/(\w+)/wist/(\d+)', ShowPeopleWistHandler, name='show-people-wist'),  
         
]

app_modules = {
    
}

app = DojangApp(
    '', __name__, handlers=app_handlers, ui_modules=app_modules,
)
