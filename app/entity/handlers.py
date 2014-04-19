# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib

from app.account.decorators import require_user
from app.account.lib import UserHandler
from app.account.models import People
from app.group.models import Group
from app.util import find_mention
from dojang.app import DojangApp
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict
from tornado.escape import utf8
from tornado.options import options
from tornado.web import UIModule, authenticated
from tornado.web import URLSpec as url

from .models import Entity


class EntityDetailHandler(UserHandler):

    def get(self, id):
        entity = Entity.query.filter_by(id=note_id).first_or_404()
        if not entity:
            self.send_error(404)
            return
        self.redirect('/%s/%d' % (entity.category, movie.id) )

app_handlers = [
    ('/(\d+)', EntityDetailHandler),
]

app_modules = {
}

app = DojangApp(
    'entity', __name__, handlers=app_handlers, ui_modules=app_modules,
)