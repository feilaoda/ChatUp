# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

from tornado.web import UIModule, authenticated
from tornado.escape import utf8
from tornado.options import options
import tornado
from dojang.app import DojangApp
from dojang.cache import autocache_get, autocache_set, autocache_incr
from dojang.database import db

from app.account.lib import UserHandler
from app.account.decorators import require_user, apiauth
from app.account.models import People
from app.group.models import Group
from app.lib.util import find_mention

from app.node.models import Node
from .models import Topic, TopicReply, TopicVote, TopicLog
from .lib import get_full_replies, get_full_topic, get_full_topics
from .lib import reply_impact_for_topic, accept_reply_impact_for_user
from .lib import up_impact_for_topic, up_impact_for_user
from .lib import down_impact_for_topic, down_impact_for_user

VOTE_UP = 1
VOTE_DOWN = 0


class AllTopicsHandler(UserHandler):

    def get(self, category="health"):
        p = self.get_argument('p', 1)
        limit = 30
        nodes = Node.query.filter_by(platform=0).all()
        node_ids = []
        for node in nodes:
            node_ids.append(node.id)
        pagination = Topic.query.filter(Topic.node_id.in_(node_ids)).order_by('-last_reply_time').paginate(p, limit)
                
        pagination.items = get_full_topics(pagination.items)

        self.render('topic/show_topic_list.html', pagination=pagination)


class TopicHandler(UserHandler):
    def get(self, id):
        topic = Topic.query.get_or_404(id)
        node = Node.query.get_or_404(topic.node_id)
        p = self.get_argument('p', 1)
        topic = get_full_topic(topic)

        pagination = TopicReply.query.filter_by(topic_id=topic.id).order_by('order')\
                .paginate(p, 50, total=topic.reply_count)
        pagination.items = get_full_replies(pagination.items)

 
        
        self.render('topic/show_topic.html', topic=topic, node=node,
                    pagination=pagination)

    def post(self, id):
        action = self.get_argument('action', 'hit')
        #: compatible for rest api
        if action == 'delete':
            self.delete(id)
            return
        if action == 'close':
            self.close_topic(id)
            return
        if action == 'promote':
            self.promote_topic(id)
            return
        #: hit count
        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        topic.hits += 1
        db.session.add(topic)
        db.session.commit()
        self.write({'stat': 'ok'})

    @require_user
    def delete(self, id):
        topic = self._get_verified_topic(id)
        if not topic:
            return
        #: delete a topic
        db.session.delete(topic)

        #: decrease node.topic_count
        node = Node.query.get_first(id=topic.node_id)
        node.topic_count -= 1
        db.session.add(node)
        db.session.commit()

        self.flash_message('Topic is deleted', 'info')
        self.redirect('/')

    @require_user
    def close_topic(self, id):
        topic = self._get_verified_topic(id)
        if not topic:
            return
        topic.status = 'close'
        db.session.add(topic)
        db.session.commit()
        self.flash_message('Topic is closed', 'info')
        self.redirect('/topic/%s' % topic.id)

    @require_user
    def promote_topic(self, id):
        topic = self._get_verified_topic(id)
        if not topic:
            return
        #: promote topic cost reputation
        user = People.query.get_first(id=topic.people_id)
        if not user:
            self.send_error(404)
            return
        if topic.status == 'promote':
            self.flash_message('Your topic is promoted', 'info')
            self.redirect('/topic/%s' % topic.id)
            return
        cost = int(options.promote_topic_cost)
        if user.reputation < cost + 20:
            self.flash_message('Your reputation is too low', 'warn')
            self.redirect('/topic/%s' % topic.id)
            return
        user.reputation -= cost
        db.session.add(user)

        topic.status = 'promote'
        topic.impact += 86400  # one day
        db.session.add(topic)
        db.session.commit()
        self.flash_message('Your topic is promoted', 'info')
        self.redirect('/topic/%s' % topic.id)

    @require_user
    def _get_verified_topic(self, id):
        #: delete topic need a password
        password = self.get_argument('password', None)
        if not password:
            self.flash_message('Password is required', 'error')
            self.redirect('/topic/%s' % id)
            return

        if not self.current_user.check_password(password):
            self.flash_message('Invalid password', 'error')
            self.redirect('/topic/%s' % id)
            return

        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        #: check permission
        if not self.check_permission_of(topic):
            return
        return topic

 

class EditTopicHandler(UserHandler):
    @require_user
    def get(self, id):
        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        self.check_permission(topic)
        if topic.hidden == 'y':
            return self.send_error(403)
            
        self.render('topic/edit_topic.html', topic=topic)

    @require_user
    def post(self, id):
        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        hidden = self.get_argument('hidden', None)
        if not title:
            self.flash_message('Please fill the title field', 'error')
            self.render('topic/edit_topic.html', topic=topic)
            return
        if not self.check_permission(topic):
            self.render('topic/edit_topic.html', topic=topic)
            return

        if hidden == 'on':
            hidden = "y"
        else:
            hidden = "n"
        topic.title = title
        topic.content = content
        topic.hidden = hidden
        db.session.add(topic)

        log = TopicLog(topic_id=topic.id, people_id=self.current_user.id)
        db.session.add(log)
        db.session.commit()

        url = '/topic/%d' % topic.id
        self.redirect(url)


class MoveTopicHandler(UserHandler):
    @require_user
    def get(self, topic_id):
        topic = Topic.query.get_first(id=topic_id)
        if not topic:
            self.send_error(404)
            return
        self.check_permission(topic)
        nodes = Node.query.all()
        self.render('topic/move_topic.html', topic=topic, nodes=nodes)

    @require_user
    def post(self, topic_id):
        node_name = self.get_argument('node_name', None)
        if not node_name:
            self.send_error(404)
            return
        topic = Topic.query.get_first(id=topic_id)
        if not topic:
            self.send_error(404)
            return
        node = Node.query.get_first(name=node_name)
        if not node:
            self.send_error(404)
            return
        #: check permission
        if not self.check_permission(topic):
            return self.send_error(403)
        
        #: increase node.topic_count
        old_node_id = topic.node_id
        old_node = Node.query.filter_by(id=topic.node_id).first_or_404()

        topic.node_id = node.id
        old_node.topic_count -= 1
        node.topic_count += 1

        db.session.add(topic)
        db.session.add(node)
        db.session.add(old_node)

        db.session.commit()
        self.redirect('/topic/%d' % topic.id)


class DeleteTopicHandler(UserHandler):
    @require_user
    def get(self, topic_id):
        topic = Topic.query.get_first(id=topic_id)
        if not topic:
            self.send_error(404)
            return
        self.check_permission(topic)
        self.render('topic/delete_topic.html', topic=topic)

    @require_user
    def post(self, topic_id):
        topic = Topic.query.get_first(id=topic_id)
        if not topic:
            self.send_error(404)
            return
        
        #: check permission
        if not self.check_permission(topic):
            return self.send_error(403)
        
        #: increase node.topic_count
        node = Node.query.filter_by(id=topic.node_id).first_or_404()
        node.topic_count -= 1

        db.session.delete(topic)
        db.session.add(node)
        db.session.commit()
        self.flash_message("delete topic %s successful" % (topic_id), "success")
        self.redirect('/node/%s' % node.name)




class CreateReplyHandler(UserHandler):
    @require_user
    def post(self, id):
        # for topic reply
        content = self.get_argument('content', None)
        hidden = self.get_argument('hidden', None)
        if not content:
            self.flash_message('Please fill the required fields', 'error')
            self.redirect('/topic/%s' % id)
            return

        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        if topic.status == 'delete':
            self.send_error(404)
            return
        if topic.status == 'close':
            self.send_error(403)
            return
    
        digest = hashlib.md5(utf8(content)).hexdigest()
        key = "r:%d:%s" % (self.current_user.id, digest)
        url = autocache_get(key)
        # avoid double submit
        if url:
            self.redirect(url)
            self.flash_message("you send a same message", "message")
            return

        user = self.current_user

        index_key = 'topic:%d'%topic.id
        index_num = autocache_get(index_key)
        if index_num is None:
            index_num = topic.reply_count
            autocache_set(index_key, index_num, 0)

        print index_num
        index_num = autocache_incr(index_key,1)
        print index_num
        if index_num is None:
            index_num = 1
            autocache_set(index_key, index_num, 0)
        #: create reply
        reply = TopicReply(topic_id=id, people_id=user.id, content=content)
        # if hidden == 'on':
        #     reply.hidden = 'y'
        # else:
        #     reply.hidden = 'n'

        # if topic.hidden == 'y' and topic.people_id == user.id:
        #     reply.hidden = 'y'
            
        #: impact on topic
        topic.reply_count = index_num
        reply.order = index_num
        #: update topic's last replyer
        topic.last_reply_by = self.current_user.id
        topic.last_reply_time = datetime.utcnow()

        db.session.add(reply)
        db.session.add(topic)
        db.session.commit()

        num = (index_num - 1) / 30 + 1
        url = '/topic/%s' % str(id)
        if num > 1:
            url += '?p=%s' % num
        autocache_set(key, url, 100)
        self.redirect("%s#reply%s" % (url, topic.reply_count))

        refer = '<a href="/topic/%s#reply-%s">%s</a>' % \
                (topic.id, topic.reply_count, topic.title)
        #: reply notification
        self.create_notification(topic.people_id, content, refer, type='reply')
        #: mention notification
        for username in set(find_mention(content)):
            self.create_notification(username, content, refer,
                                     exception=topic.people_id)

        db.session.commit()
        #TODO: social networks


#: /reply/$id
class ReplyHandler(UserHandler):
    """ReplyHandler

    - POST: for topic owner to accept a reply.
    - DELETE: for reply owner to delete a reply.
    """
    @authenticated
    def delete(self, reply_id):
        #: delete a reply by reply owner
        reply = TopicReply.query.get_first(id=reply_id)
        if not reply:
            self.set_status(404)
            self.write({'stat': 'fail', 'msg': 'reply not found'})
            return
        if self.current_user.is_staff or self.current_user.id == reply.people_id:
            topic = Topic.query.get_first(id=reply.topic_id)
            if topic and topic.reply_count:
                topic.reply_count -= 1
            db.session.delete(reply)
            db.session.add(topic)
            db.session.commit()
            self.write({'stat': 'ok'})
            return
        self.set_status(403)
        self.write({'stat': 'fail', 'msg': 'permission denied'})


class VoteTopicHandler(UserHandler):
    @apiauth
    def post(self, id):
        _ = self.locale.translate
        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        if topic.people_id == self.current_user.id:
            # you can't vote your own topic
            dct = {'result': 'fail', 'msg': _("Can't vote your own topic")}
            self.write(dct)
            return
        action = self.get_argument('action', None)
        if not action:
            self.send_error(403)
            return
        if action == 'up':
            self.up_topic(topic)
            return
        if action == 'down':
            self.down_topic(topic)
            return
        self.send_error('403')
        return

    def up_topic(self, topic):
        _ = self.locale.translate
        user = self.current_user
        vote = TopicVote.query.get_first(people_id=user.id, topic_id=topic.id)
        owner = People.query.get_first(id=topic.people_id)
        if not vote:
            vote = TopicVote(people_id=user.id, topic_id=topic.id, value=VOTE_UP)
            db.session.add(vote)
            # db.session.commit()
            self._active_up(topic, owner, user.reputation)
            return
        #: cancel vote
        if vote.value == VOTE_UP:
            # vote.type = 'none'
            db.session.delete(vote)
            # db.session.commit()
            self._cancle_up(topic, owner, user.reputation)
            return
        #: change vote
        # if vote.value == VOTE_DOWN:
        #     vote.valule = VOTE_UP
        #     db.session.add(vote)
        #     db.session.commit()
        #     self.write({'stat': 'fail', 'msg': _("Cancel your vote first")})
        #     return
        #: vote
        vote.valule = VOTE_UP
        db.session.add(vote)
        # db.session.commit()
        self._active_up(topic, owner, user.reputation)
        return

    def _active_up(self, topic, owner, reputation):
        #: increase topic's impact
        topic.impact += up_impact_for_topic(reputation)
        topic.up_count += 1
        db.session.add(topic)
        #: increase topic owner's reputation
        # owner.reputation += up_impact_for_user(reputation)
        # db.session.add(owner)
        db.session.commit()
        self.write({'result': 'ok', 'data': topic.up_count})
        return

    def _cancle_up(self, topic, owner, reputation):
        topic.impact -= up_impact_for_topic(reputation)
        topic.up_count -= 1
        db.session.add(topic)
        # owner.reputation -= up_impact_for_user(reputation)
        # db.session.add(owner)
        db.session.commit()
        self.write({'result': 'ok', 'data': topic.up_count})
        return

    def down_topic(self, topic):
        _ = self.locale.translate
        user = self.current_user
        vote = TopicVote.query.get_first(people_id=user.id, topic_id=topic.id)
        owner = People.query.get_first(id=topic.people_id)
        if not vote:
            vote = TopicVote(people_id=user.id, topic_id=topic.id, value=VOTE_DOWN)
            db.session.add(vote)
            self._active_down(topic, owner, user.reputation)
            return
        #: cancel vote
        if vote.value == VOTE_DOWN:
            # vote.type = 'none'
            db.session.delete(vote)
            self._cancel_down(topic, owner, user.reputation)
            return

        #: change vote
        # if vote.type == 'up':
        #     self.write({'stat': 'fail', 'msg': _("Cancel your vote first")})
        #     return

        vote.value = VOTE_DOWN
        db.session.add(vote)
        self._active_down(topic, owner, user.reputation)
        return

    def _active_down(self, topic, owner, reputation):
        #: increase topic's impact
        topic.impact -= down_impact_for_topic(reputation)
        topic.down_count += 1
        db.session.add(topic)
        #: increase topic owner's reputation
        # owner.reputation -= down_impact_for_user(reputation)
        # db.session.add(owner)
        db.session.commit()
        self.write({'result': 'ok', 'data': topic.down_count})
        return

    def _cancel_down(self, topic, owner, reputation):
        topic.impact += down_impact_for_topic(reputation)
        topic.down_count -= 1
        db.session.add(topic)
        # owner.reputation += down_impact_for_user(reputation)
        # db.session.add(owner)
        db.session.commit()
        self.write({'result': 'ok', 'data': topic.down_count})
        return


app_handlers = [
    ('', AllTopicsHandler),
    ('/([a-z]+)', AllTopicsHandler),
    ('/(\d+)', TopicHandler),
    ('/(\d+)/edit', EditTopicHandler),
    ('/(\d+)/move', MoveTopicHandler),
    ('/(\d+)/delete', DeleteTopicHandler),
    ('/(\d+)/reply', CreateReplyHandler),
    ('/(\d+)/vote', VoteTopicHandler),
]


class UserModule(UIModule):
    """UserModule

    This module contains topic and reply count,
    in this case, it is located in topic app
    """
    def render(self, people_id):
        user = People.query.get_first(id=people_id)
        if not user:
            return ''
        topic_count = Topic.query.filter_by(people_id=people_id).count()
        reply_count = TopicReply.query.filter_by(people_id=people_id).count()
        user.topic_count = topic_count
        user.reply_count = reply_count
        return self.render_string('module/user.html', user=user)

def topiclink(topic):
    return "/topic/%d" % topic.id

class ShowTopicModule(UIModule):
    def render(self, topic):
        return self.render_string('topic/show_topic_module.html', topic=topic, topiclink=topiclink, locale=tornado.locale)

class ShowTopicListModule(UIModule):
    def render(self, topics):
        return self.render_string('topic/show_topic_list_module.html', topics=topics)



app_modules = {
    'ShowTopic':ShowTopicModule,
    'ShowTopicList':ShowTopicListModule
}

app = DojangApp(
    'topic', __name__, handlers=app_handlers, ui_modules=app_modules
)
