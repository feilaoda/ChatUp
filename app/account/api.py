from datetime import datetime
import hashlib

from app.account.decorators import require_user, apiauth
from app.account.lib import SimpleApiHandler, CheckMixin
from app.account.models import People
from dojang.app import DojangApp
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.util import ObjectDict
from dojang.web import ApiHandler
import errors
from tornado import escape
from tornado.options import options
from tornado.web import UIModule 
from tornado.web import URLSpec as url

from . import validators
from .models import People


class SigninHandler(SimpleApiHandler):
    def get(self):
        return self.post()
        
    def post(self):
        account = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if not (account and password):
            return self.render_json(result=errors.AccountNotFound)

        if '@' in account:
            user = People.query.filter_by(email=account).first()
        else:
            user = People.query.filter_by(username=account).first()
        if user and user.check_password(password):
            self.set_secure_cookie('user', '%s/%s' % (user.id, user.token), domain=options.cookie_domain)
            r=dict()
            r['people_id'] = user.id
            return self.render_json(data=r)
            
        return self.render_json(result=errors.PasswordError)

class SignupHandler(SimpleApiHandler):
    def signup_token(username,salt,secret, token):
        hsh = hashlib.sha1(salt + username + secret).hexdigest()
        if hsh == token:
            return True
        else:
            return False

    def get(self):
        username = self.get_argument('username', '')
        english_name = self.get_argument('english_name', None)
        password = self.get_argument('password', None)
        salt = self.get_argument('salt', None)
        token = self.get_argument('token', None)

        # if token is None or not signup_token(username, salt, options.api_secret, token):
        #     self.render_json(result=errors.UnknowError)
        #     return

        if not validators.username(username, min=3, max=20):
            self.render_json(result=errors.UserNameNotAllowed)
            return

        people = People.query.filter_by(username=username).first()
        if people:
            self.render_json(result=errors.UserNameAlreadyExists)
            return

        user = People(username)
        user.nickname = english_name
        user.password = user.create_password(password)
        db.session.add(user)
        db.session.commit()

        self.set_secure_cookie('user', '%s/%s' % (user.id, user.token), domain=options.cookie_domain)
        
        r=dict()
        r['people_id'] = user.id
        self.render_json(data=r)


api_handlers = [
    
    url('/signin', SigninHandler),  #v1/account/signin
    url('/signup', SignupHandler),  #v1/account/signup

]


app = DojangApp(
    'account', __name__, version="v1", handlers=api_handlers
)
