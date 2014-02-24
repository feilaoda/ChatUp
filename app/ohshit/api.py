# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import logging
import os
import time
import json

from app.account.decorators import require_user, apiauth
from app.account.lib import SimpleApiHandler, CheckMixin
from app.account.models import People
from app.node.models import Node
from dojang.app import DojangApp
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict, create_token
from dojang.web import ApiHandler
from dojang.cache import complex_cache

from tornado import escape
from tornado.options import options
from tornado.web import UIModule 
from tornado.web import URLSpec as url


class GetGroupListHandler(SimpleApiHandler):
    # @apiauth
    def get(self):
        pass

api_handlers = [
  
]

#api.iosplay.com/v1/wepusher/(\d+)
app = DojangApp(
    'ohshit', __name__, version="v1", handlers=api_handlers
)

