import json

from dojang.cache import get_cache_list, autocache_hdel
from dojang.database import db
from dojang.web import DojangHandler, OAuthRequestHandler
from sqlalchemy import exc as sa_exc
from tornado.options import options
from tornado.web import HTTPError,RequestHandler

from .models import People, Notify, Social


class CheckMixin(object):
    def check_permission(self, model):
        user = self.current_user
        if model.people_id == user.id or user.is_admin:
            return True
        self.flash_message(
            "You have no permission",
            "warn"
        )
        self.send_error(403)
        return False

    def people_is_master(self, people):
        if self.current_user and people and self.current_user.id == people.id:
            return True
        return False

class UserHandler(DojangHandler, CheckMixin):
    def finish(self, chunk=None):
        try:
            super(DojangHandler, self).finish(chunk);
        except sa_exc.SQLAlchemyError, e:
            db.session.rollback()
        else:
            pass
        finally:
            pass
    def raise_error(self, code):
        raise HTTPError(code)
        
    # def finish(self, chunk=None):
    #     super(UserHandler, self).finish(chunk)
    #     if self.get_status() == 500:
    #         try:
    #             db.session.rollback()
    #         except:
    #             #db.session.rollback()
    #             pass
    #         #finally:
    #         #    self.db.commit()


    def get_current_user(self):
        cookie = self.get_secure_cookie("user")
        if not cookie:
            return None
        try:
            id, token = cookie.split('/')
            id = int(id)
        except:
            self.clear_cookie("user")
            return None
        user = People.query.filter_by(id=id).first()
        if not user:
            return None
        if token == user.token:
            return user
        self.clear_cookie("user")
        return None

    @property
    def next_url(self):
        next_url = self.get_argument("next", None)
        return next_url or '/'

    def clear_people_cache(self,people_id):
        autocache_hdel('h:people', people_id)


    def create_notification(self, receiver, content, refer, **kwargs):
        if not self.current_user:
            return
        if not isinstance(receiver, (int, long)):
            # receiver is username
            receiver = People.query.filter_by(username=receiver).value('id')

        if not receiver:
            # self.flash_message('There is no such people', 'error')
            return
        if receiver == self.current_user.id:
            #: can't send notification to oneself
            return
        if 'exception' in kwargs and receiver == kwargs['exception']:
            return

        data = Notify(sender=self.current_user.id, receiver=receiver,
                            content=content, refer=refer)
        if 'type' in kwargs:
            data.type = kwargs['type']
        db.session.add(data)


def get_full_notifies(messages):
    users = get_cache_list(People, (m.sender for m in messages), 'member:')
    for msg in messages:
        if msg.sender in users:
            msg.who = users[msg.sender]
            yield msg


def get_social_map(user_id):
    dct = {}
    for network in Social.query.filter_by(user_id=user_id):
        dct[network.service] = network

    return dct


class SimpleApiHandler(UserHandler):
    def check_xsrf_cookie(self):
        pass

    def render_json(self, result="200", message=None, data=None):
        if isinstance(result, (dict, list)):
            data = result
            result = "200"

        res = dict()
        if result == "ok":
            result = "200"
            
        if result != "200":
            return self.raise_error(result)
        res['result'] = result
        if message:
            res['message'] = message
        if data:
            res['data'] = data
        return super(SimpleApiHandler,self).render_json(res)


class OAuthApiRequestHandler(OAuthRequestHandler):
    
    def get_client(self):

        if not isinstance(request, oauth.Request):
            request = self.get_oauth_request()
        client_key = request.get_parameter('oauth_consumer_key')
        if not client_key:
            raise Exception('Missing "oauth_consumer_key" parameter in ' \
                'OAuth "Authorization" header')

        client = models.Client.get_by_key_name(client_key)
        if not client:
            raise Exception('Client "%s" not found.' % client_key)

        return client