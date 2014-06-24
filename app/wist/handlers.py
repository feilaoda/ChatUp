# -*- coding: utf-8 -*-
from dojang.app import DojangApp
from app.account.lib import UserHandler	

from .models import Wist


class AllWistsHandler(UserHandler):

    def get(self):
        p = self.get_argument('p', 1)
        limit = 30
        pagination = Wist.query.filter().order_by('-id').paginate(p, limit)

        self.render('wist/show_wist.html', pagination=pagination)


class ShowWistHandler(UserHandler):
	def get(self, id):
		wist = Wist.query.filter(id=id).first_or_404()

		self.render('wist/show_wist.html', wist=wist)


app_handlers = [
    ('', AllWistsHandler),
    
]


app_modules = {
    
}

app = DojangApp(
    'wist', __name__, handlers=app_handlers, ui_modules=app_modules
)