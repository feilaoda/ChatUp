# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url
from tornado.escape import utf8
from tornado.options import options

from dojang.app import DojangApp
from dojang.util import ObjectDict
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.cache import autocached, complex_cache_del

from app.account.lib import UserHandler
from app.account.decorators import require_user
from app.account.models import People
from app.group.models import Group

from app.note.models import Note, PERMISSION_PUBLIC



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



class ShowPeopleNotesHandler(PeopleHandler):

    def get(self, people_id):
        people_id = int(people_id)
        if self.current_user and self.current_user.id == people_id:
            notes = Note.query.filter_by(people_id=people_id).all()
            people=self.current_user
        else:
            notes = Note.query.filter_by(people_id=people_id, permission=PERMISSION_PUBLIC).all()
            people = People.query.filter_by(id=people_id).first_or_404()

        self.render('people/show_people_notes.html', people=people, notes=notes)




class ShowPeopleUsernameHandler(PeopleHandler):
    def get(self, username):
        people = People.query.filter_by(username=username).first_or_404()
        return self.redirect('/people/%d' % (people.id))


app_handlers = [
    url('/(\d+)/notes', ShowPeopleNotesHandler, name='show-people-notes'),
    url('/(\d+)', ShowPeopleHandler, name='show-people'),
    url('/u/(\w+)', ShowPeopleUsernameHandler, name='show-people-username'),    
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
    'people', __name__, handlers=app_handlers, ui_modules=app_modules,
)