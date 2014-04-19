# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib

from app.account.decorators import require_user, require_admin
from app.account.lib import UserHandler
from app.account.models import People
from dojang.app import DojangApp
from dojang.cache import cached
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict
from tornado.escape import utf8
from tornado.options import options
from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url


class AboutHandler(UserHandler):
    def get(self):
        self.render('about.html')


app_handlers = [
    url('', AboutHandler, name='about-show'),
]



app_modules = {
   
}



app = DojangApp(
    'about', __name__, handlers=app_handlers, ui_modules=app_modules,
)
