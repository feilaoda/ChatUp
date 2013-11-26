# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url
from tornado.escape import utf8
from tornado.options import options

from dojang.app import DojangApp
from dojang.util import ObjectDict
from dojang.cache import cached
from dojang.database import db
from dojang.mixin import ModelMixin

from app.account.lib import UserHandler
from app.account.decorators import require_user, require_admin
from app.account.models import People

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
