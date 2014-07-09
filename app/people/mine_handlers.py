# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib

from app.account.decorators import require_user
from app.account.lib import UserHandler
from app.account.models import People
from app.group.models import Group
from dojang.app import DojangApp
from dojang.cache import autocached
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict
from tornado.escape import utf8
from tornado.options import options
from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url

from wist_handlers import app_handlers as wist_handlers

class PeopleHandler(UserHandler):


    #@autocached(prefix=CacheMovieWatchListPrefix, time=60*60*24*7)
    def filter_watch_movies(self, people_id, watch, page_num):
        
        limit = 20
        pagination = MovieWatchList.query.filter_by(people_id=people_id, watch=watch).order_by('-id').paginate(page_num, limit)
        ids = []
        movies = []
        if pagination:
            for w in pagination.items:
                movies.append(w.movie)
        pagination.items = movies
        return pagination


class ShowPeopleHandler(PeopleHandler):

    def get(self, people_id):
        people_id = int(people_id)
        if self.current_user and self.current_user.id == people_id:
            people=self.current_user
        else:
            people = People.query.filter_by(id=people_id).first_or_404()

        self.render('people/show_people.html', people=people)


class ShowPeopleUsernameHandler(PeopleHandler):
    def get(self, username):
        people = People.query.filter_by(username=username).first_or_404()
        return self.render('people/show_people.html', people=people)




app_handlers = [
    url('/people/(\d+)', ShowPeopleHandler, name='show-people'),
    url('/(\w+)', ShowPeopleUsernameHandler, name='show-people-username'),    
]

class RecentPeoplesModule(UIModule):
    def render(self):
        users = People.query.order_by('-id').limit(12)
        return self.render_string('module/people_cell.html', users=users)


app_modules = {
    'RecentPeoples': RecentPeoplesModule,
}

class RecentPeoplesHandler(UserHandler):
    def head(self):
        pass

    def get(self):
        p = self.get_argument('p', 1)
        pagination = People.query.order_by('-reputation').paginate(p, 80)
        self.render('people_list.html', pagination=pagination)

class CityPeoplesHandler(UserHandler):
    def head(self):
        pass

    def get(self, city):
        p = self.get_argument('p', 1)
        pagination = People.query.filter_by(city=city)\
                .order_by('-reputation').paginate(p, 80)
        self.render('people_list.html', pagination=pagination)


app = DojangApp(
    '', __name__, handlers=app_handlers, ui_modules=app_modules,
)