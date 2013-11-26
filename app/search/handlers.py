# -*- coding: utf-8 -*-
#!/usr/bin/env python


import hashlib
from datetime import datetime
import formencode

from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url
from tornado.escape import utf8
from tornado.options import options

from dojang.app import DojangApp
from dojang.util import ObjectDict
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.form import FormSchema
from dojang.cache import autocached

from app.account.lib import UserHandler, SimpleApiHandler
from app.account.decorators import require_user, require_admin
from app.account.models import People
from app.group.models import Group
from app.lib.util import find_mention

from .models import SearchMovie


class SearchHandler(UserHandler):
    pass



class SearchMovieHandler(SearchHandler, BoardMixin):

    @autocached(prefix="m:search", time=3600)
    def search_movie(self, q):
        limit = 20
        search_movies = SearchMovie.query.filter_by(title__contains=q).limit(limit).all()
        movie_ids = []
        for s in search_movies:            
            movie_ids.append(s.movie_id)
        return movie_ids

    def get(self):
        q = self.get_argument('q', '')
        if len(q) > 100:
            q = q[:100]
        movie_ids = self.search_movie(q)
        # search_movies = SearchMovie.query.filter_by(title__contains=q).all()
        # movie_ids = []
        # for s in search_movies:            
        #     movie_ids.append(s.movie_id)
        movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
         
        boards = self.find_current_boards()
        self.render('search/movie.html', movies=movies, boards=boards)


app_handlers = [
    url('', SearchMovieHandler, name='search-movie'),
]


app_modules = {
}



app = DojangApp(
    'search', __name__, handlers=app_handlers, ui_modules=app_modules,
)




