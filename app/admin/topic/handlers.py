# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

from tornado.web import UIModule, authenticated
from tornado.escape import utf8
from tornado.options import options
import tornado
from dojang.app import DojangApp
from dojang.cache import autocache_get, autocache_set, autocache_incr, autocache_hdel
from dojang.database import db

from app.account.lib import UserHandler
from app.account.decorators import require_staff, require_admin, require_user, apiauth
from app.account.models import People
from app.group.models import Group
from app.lib.util import find_mention

from app.node.models import Node
from app.topic.models import Topic, TopicReply, TopicVote, TopicLog
from app.topic.lib import get_full_replies, get_full_topic, get_full_topics
from app.topic.lib import reply_impact_for_topic, accept_reply_impact_for_user
from app.topic.lib import up_impact_for_topic, up_impact_for_user
from app.topic.lib import down_impact_for_topic, down_impact_for_user

VOTE_UP = 1
VOTE_DOWN = 0

SAMPLE_PEOPLE=3

class AllTopicsHandler(UserHandler):
    def get(self):
        self.render('admin/topic/all_topics.html')

class ShowTopicHandler(UserHandler):
    def get(self, id):
        topic = Topic.query.get_or_404(id)
        node = Node.query.get_or_404(topic.node_id)
        p = self.get_argument('p', 1)
        topic = get_full_topic(topic)

        pagination = TopicReply.query.filter_by(topic_id=topic.id).order_by('order').paginate(p, 50, total=topic.reply_count)
        pagination.items = get_full_replies(pagination.items)

        peoples = People.query.filter_by(role=SAMPLE_PEOPLE).all()
        
        self.render('admin/topic/show_topic.html', topic=topic, node=node,
                    pagination=pagination, peoples=peoples)

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


class CreateTopicHandler(UserHandler):
    @require_staff
    def get(self):
        topic = Topic()
        nodes = Node.query.all()
        peoples = People.query.filter_by(role=SAMPLE_PEOPLE).all()

        self.render('admin/topic/create_topic.html', topic=topic, nodes=nodes, peoples=peoples)

    @require_staff
    def post(self):
        node_name = self.get_argument('node_name')
        people_id = self.get_argument('people_id')
        node = Node.query.get_first(name=node_name)
        people = People.query.filter_by(id=people_id).first_or_404()
        if not node:
            self.send_error(404)
            return
        
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        hidden =  self.get_argument('hidden', None)
        topic = Topic()
        if not title:
            self.flash_message('Please fill the title field', 'error')
            self.render('admin/topic/create_topic.html', topic=topic)
            return
        
        #: avoid double submit
         
        digest = hashlib.md5(utf8(title)).hexdigest()
        key = "r:%d:%s" % (people.id, digest)
        url = autocache_get(key)
        if url:
            self.redirect(url)
            return

        if hidden == 'on':
            hidden = "y"
        else:
            hidden = "n"

        topic.title = title
        topic.content = content
        topic.node_id = node.id
        topic.people_id = people.id
        topic.hidden = hidden
        node.topic_count += 1
        db.session.add(topic)
        db.session.add(node)
        db.session.commit()

        url = '/topic/%d' % topic.id
        # autocache_set(key, url, 100)
        self.redirect(url)

        #: notification
        refer = '<a href="/topic/%s">%s</a>' % (topic.id, topic.title)
        for username in set(find_mention(title)):
            self.create_notification(username, title, refer,
                                     exception=topic.people_id)
        for username in set(find_mention(content)):
            self.create_notification(username, content, refer,
                                     exception=topic.people_id)


class EditTopicHandler(UserHandler):
    @require_staff
    def get(self, id):
        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        # self.check_permission(topic)
        self.render('topic/edit_topic.html', topic=topic)

    @require_staff
    def post(self, id):
        topic = Topic.query.get_first(id=id)
        if not topic:
            self.send_error(404)
            return
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        if not title:
            self.flash_message('Please fill the title field', 'error')
            self.render('topic/edit_topic.html', topic=topic)
            return
        # if not self.check_permission(topic):
        #     self.render('topic/edit_topic.html', topic=topic)
        #     return

        topic.title = title
        topic.content = content
        db.session.add(topic)

        log = TopicLog(topic_id=topic.id, people_id=self.current_user.id)
        db.session.add(log)
        db.session.commit()

        url = '/topic/%d' % topic.id
        self.redirect(url)


class MoveTopicHandler(UserHandler):
    @require_staff
    def get(self, topic_id):
        topic = Topic.query.get_first(id=topic_id)
        if not topic:
            self.send_error(404)
            return
        # self.check_permission(topic)
        nodes = Node.query.all()
        self.render('topic/move_topic.html', topic=topic, nodes=nodes)

    @require_staff
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
        # if not self.check_permission(topic):
        #     return self.send_error(403)
        
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
    @require_admin
    def get(self, topic_id):
        topic = Topic.query.get_first(id=topic_id)
        if not topic:
            self.send_error(404)
            return
        # self.check_permission(topic)
        self.render('topic/delete_topic.html', topic=topic)

    @require_admin
    def post(self, topic_id):
        topic = Topic.query.get_first(id=topic_id)
        if not topic:
            self.send_error(404)
            return
        
        #: check permission
        # if not self.check_permission(topic):
        #     return self.send_error(403)
        
        #: increase node.topic_count
        node = Node.query.filter_by(id=topic.node_id).first_or_404()
        node.topic_count -= 1

        db.session.delete(topic)
        db.session.add(node)
        db.session.commit()
        self.flash_message("delete topic %s successful" % (topic_id), "success")
        self.redirect('/node/%s' % node.name)




class CreateReplyHandler(UserHandler):
    @require_staff
    def post(self, id):
        content = self.get_argument('content', None)
        hidden = self.get_argument('hidden', None)
        people_id = self.get_argument('people_id', None)
        if not content:
            self.flash_message('Please fill the required fields', 'error')
            self.redirect('/topic/%s' % id)
            return

        user = People.query.filter_by(id=people_id).first_or_404()

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
        key = "reply:%d:%s" % (user.id, digest)
        url = autocache_get(key)
        # avoid double submit
        if url:
            self.redirect(url)
            return

        

        index_key = 'topic:%d'%topic.id
        index_num = autocache_get(index_key)
        if index_num is None:
            index_num = topic.reply_count
            autocache_set(index_key, index_num)

        index_num = autocache_incr(index_key,1)
        

        #: create reply
        reply = TopicReply(topic_id=id, people_id=user.id, content=content)
        if hidden == 'on':
            reply.hidden = 'y'
        else:
            reply.hidden = 'n'

        #: impact on topic
        topic.reply_count = index_num
        reply.order = index_num

        #: update topic's last replyer
        topic.last_reply_by = user.id
        topic.last_reply_time = datetime.utcnow()

        db.session.add(reply)
        db.session.add(topic)
        db.session.commit()

        num = (topic.reply_count - 1) / 30 + 1
        url = '/admin/topic/%s' % str(id)
        if num > 1:
            url += '?p=%s' % num
        autocache_set(key, url, 100)
        

        refer = '<a href="/topic/%d#reply-%d">%s</a>' % \
                (topic.id, reply.order, topic.title)
        #: reply notification
        self.create_notification(topic.people_id, content, refer, type='reply')
        #: mention notification
        for username in set(find_mention(content)):
            self.create_notification(username, content, refer,
                                     exception=topic.people_id)

        db.session.commit()
        #TODO: social networks
        self.redirect("%s#reply%s" % (url, topic.reply_count))


#: /reply/$id
class DeleteReplyHandler(UserHandler):
    """ReplyHandler

    - POST: for topic owner to accept a reply.
    - DELETE: for reply owner to delete a reply.
    """
    @require_user
    def get(self, topic_id, reply_id):
        #: delete a reply by reply owner
        reply = TopicReply.query.get_first(id=reply_id)
        if not reply:
            self.set_status(404)
            self.write({'stat': 'fail', 'msg': 'reply not found'})
            return
        if self.current_user.is_admin or self.current_user.id == reply.people_id:
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



app_handlers = [
    ('', AllTopicsHandler),
    ('/new', CreateTopicHandler),
    ('/(\d+)', ShowTopicHandler),
    ('/(\d+)/edit', EditTopicHandler),
    ('/(\d+)/move', MoveTopicHandler),
    ('/(\d+)/delete', DeleteTopicHandler),
    ('/(\d+)/reply', CreateReplyHandler),
    ('/(\d+)/reply/(\d+)/delete', DeleteReplyHandler),
]

app = DojangApp(
    'admin/topic', __name__, handlers=app_handlers, 
)
