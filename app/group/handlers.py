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

from app.util import find_mention
from .models import Group, GroupFollow


PublicGroup = 0
InvitedGroup = 1

class RecentGroupsHandler(UserHandler):
    
    def get(self):
        groups = Group.query.filter_by(status=1).all()
        self.render('group/recent_groups.html', groups=groups)


class NewGroupHandler(UserHandler):
    @authenticated
    def get(self):
        group = ObjectDict()
        self.render('group/create_group.html', group=group)

    @authenticated
    def post(self):
        o = ObjectDict()
        o.title = self.get_argument('title', None)
        o.description = self.get_argument('description', None)
        o.permission = self.get_argument('permission', None)
        # o.color = self.get_argument('color', None)
        o.tag = self.get_argument('tag', None)

        if not (o.title and o.description):
            self.flash_message('Please fill the required field', 'error')
            self.render('group/create_group.html', group=o)
            return

        group = Group(**o)
        group.people_id = self.current_user.id

        db.session.add(group)
        db.session.commit()

        self.reverse_redirect('group')


class EditGroupHandler(UserHandler,  ModelMixin):
    
    @authenticated
    def get(self, group_id=None):
        group = Group.query.filter_by(id=group_id).first_or_404()
        if not group:
            self.send_error(404)
            return
        self.render('group/edit_group.html', group=group)

    @authenticated
    def post(self, group_id):
        group = Group.query.filter_by(id=group_id).first()
        if not group:
            self.send_error(404)
            return
        self.update_model(group, 'title', True)
        self.update_model(group, 'description', True)
        self.update_model(group, 'permission')
        self.update_model(group, 'tag')
        # self.update_model(group, 'color')

   

        db.session.add(group)
        db.session.commit()

        self.redirect('/group/%d' % group.id)


class FollowGroupHandler(UserHandler):
    """Toggle following"""

    @authenticated
    def get(self, group_id):
        group = Group.query.filter_by(id=group_id).first_or_404()
        if group.permission != PublicGroup:
            self.flash_message("Only invited people can join in", "error")
            return
        user = self.current_user
        follow = GroupFollow.query.get_first(people_id=user.id, group_id=group.id)
        if follow:
            self.write({'stat': 'ok', 'data': 'You have followed the group'})
            return
        follow = GroupFollow(people_id=self.current_user.id, group_id=group.id)
        db.session.add(follow)
        db.session.commit()
        self.write({'stat': 'ok', 'data': 'followed'})


class UnfollowGroupHandler(UserHandler):
    """Toggle following"""

    @authenticated
    def post(self, group_id):
        group = Group.query.filter_by(id=group_id).first_or_404()
        
        user = self.current_user
        follow = FollowGroup.query.get_first(people_id=user.id, group_id=group.id)
        if follow:
            db.session.delete(follow)
            db.session.commit()
            self.write({'stat': 'ok', 'data': 'unfollow'})
            return

        self.write({'stat': 'ok', 'data': "You havn't followed the group"})

class ShowGroupHandler(UserHandler):
    def get(self, group_id=None):
        group = Group.query.filter_by(id=group_id).first_or_404()
        if not group:
            self.send_error(404)
            return
        self.render('group/show_group.html', group=group)
 

app_handlers = [
    url('', RecentGroupsHandler, name='group'),
    url('/new', NewGroupHandler, name='new-group'),
    url('/(\d+)/edit', EditGroupHandler, name='edit-group'),    
    url('/(\d+)/follow', FollowGroupHandler, name='follow-group'),
    url('/(\d+)', ShowGroupHandler, name='show-group'),
]

class GroupHeaderModule(UIModule):    
    def render(self, group):
        if not group:
            return ''
        return self.render_string('module/group_header.html', group=group)


app_modules = {
    'GroupHeader': GroupHeaderModule,
}



app = DojangApp(
    'group', __name__, handlers=app_handlers, ui_modules=app_modules,
)