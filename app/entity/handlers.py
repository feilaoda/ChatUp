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

from app.account.lib import UserHandler
from app.account.decorators import require_user
from app.account.models import People
from app.group.models import Group
from app.util import find_mention

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