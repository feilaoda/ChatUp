import hashlib
from datetime import datetime

from tornado.web import UIModule 
from tornado.web import URLSpec as url
from tornado import escape
from tornado.options import options

from dojang.app import DojangApp
from dojang.util import ObjectDict
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.web import ApiHandler
from dojang.cache import cached, autocached, complex_cache, complex_cache_del

from app.account.lib import SimpleApiHandler, CheckMixin
from app.account.decorators import require_user, apiauth
from app.account.models import People

class ShowPeopleHandler(SimpleApiHandler):

    def get(self):
        people_id = self.get_argument('people_id',None)
        people = People.query.filter_by(id=people_id).first()
        if people is None:
            return self.render_json(result=404)
        return self.render_json(data=people.to_dict())

class FollowCreatePeopleHandler(SimpleApiHandler):
    @apiauth
    def post(self):
        people_id = self.get_argument('people_id',None)
        people = self.current_user
        target = People.query.filter_by(id=people_id).first()
        if target is None:
            return self.render_json(result=404)
        if people.id == target.id:
            return self.render_json(result=403)
        follower = PeopleFollower.query.filter_by(people_id=people.id, target_id=target.id).first()
        if follower is None:
            follower = PeopleFollower()
            follower.people_id = people.id
            follower.target_id = target.id
            people.follow_count += 1
            target.followed_count += 1

            db.session.add(follower)
            db.session.add(people)
            db.session.add(target)
            db.session.commit()

        return self.render_json(result=200)

class FollowDestroyPeopleHandler(SimpleApiHandler):
    @apiauth
    def post(self):
        id = self.get_argument('uid',None)
        people = self.current_user
        target = People.query.filter_by(id=id).first()
        if target is None:
            return self.render_json(result=404)
        if people.id == target.id:
            return self.render_json(result=403)
        follower = PeopleFollower.query.filter_by(people_id=people.id, target_id=target.id).first()
        if follower:
            people.follow_count -= 1
            target.followed_count -= 1
            db.session.delete(follower)
            db.session.add(people)
            db.session.add(target)
            db.session.commit()
        return self.render_json(result=200)


api_handlers = [
    url('/show', ShowPeopleHandler),    #v1/people/show?uid=1
    url('/friendship/create', FollowCreatePeopleHandler),  #v1/people/friendship/create?uid=1
    url('/friendship/destroy', FollowDestroyPeopleHandler),  #v1/people/friendship/destroy?uid=1
]


app = DojangApp(
    'people', __name__, version="v1", handlers=api_handlers
)
