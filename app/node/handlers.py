import formencode
import tornado.web
import hashlib
from tornado.escape import utf8
from tornado.web import URLSpec as url
from tornado.web import UIModule, authenticated
from dojang.app import DojangApp
from dojang.database import db
from dojang.mixin import ModelMixin
from dojang.cache import autocache_get, autocache_set

from app.account.decorators import require_user, require_admin
from app.account.lib import UserHandler
from .models import FollowNode, Node
from app.topic.models import Topic
from app.topic.lib import get_full_topics
from app.lib.util import find_mention

class CreateNodeHandler(UserHandler):
    @require_admin
    def get(self):
        node = Node()
        self.render('node/create_node.html', node=node)

    @require_admin
    def post(self):
        o = Node()
        o.title = self.get_argument('title', None)
        o.name = self.get_argument('name', None)
        o.avatar = self.get_argument('avatar', None)
        o.description = self.get_argument('description', None)
        # o.fgcolor = self.get_argument('fgcolor', None)
        # o.bgcolor = self.get_argument('bgcolor', None)
        # o.header = self.get_argument('header', None)
        # o.sidebar = self.get_argument('sidebar', None)
        # o.footer = self.get_argument('footer', None)

        try:
            o.limit_role = int(self.get_argument('role', 0))
        except:
            o.limit_role = 0

        if not (o.name and o.title and o.description):
            self.flash_message('Please fill the required field', 'error')
            self.render('node/create_node.html', node=o)
            return

        
        o.category = self.get_argument('category', None)
        o.platform = self.get_argument('platform', 0)
        db.session.add(o)
        db.session.commit()

        self.redirect('/node/%s' % o.name)


class EditNodeHandler(UserHandler, ModelMixin):
    @require_admin
    def get(self, name):
        node = Node.query.filter_by(name=name).first_or_404()
        self.render('node/edit_node.html', node=node)

    @require_admin
    def post(self, name):
        node = Node.query.filter_by(name=name).first()
        if not node:
            self.send_error(404)
            return
        self.update_model(node, 'title', True)
        self.update_model(node, 'name', True)
        self.update_model(node, 'avatar')
        self.update_model(node, 'description', True)
        
        node.category = self.get_argument('category', None)
        node.platform = self.get_argument('platform', 0)

        try:
            node.limit_role = int(self.get_argument('role', 0))
        except:
            node.limit_role = 0

        db.session.add(node)
        db.session.commit()

        self.redirect('/node/%s' % node.name)



class FollowNodeHandler(UserHandler):
    """Toggle following"""

    @authenticated
    def post(self, name):
        node = Node.query.filter_by(name=name).first_or_404()

        user = self.current_user
        follow = FollowNode.query.get_first(people_id=user.id, node_id=node.id)
        if follow:
            db.session.delete(follow)
            db.session.commit()
            self.write({'stat': 'ok', 'data': 'unfollow'})
            return
        follow = FollowNode(people_id=self.current_user.id, node_id=node.id)
        db.session.add(follow)
        db.session.commit()
        self.write({'stat': 'ok', 'data': 'follow'})



class ShowNodeHandler(UserHandler):
 

    def get(self, name):
        node = Node.query.filter_by(name=name).first_or_404()

        p = self.get_argument('p', 1)
        pagination = Topic.query.filter_by(node_id=node.id)\
                .order_by('-last_reply_time').paginate(p, 30)
        pagination.items = get_full_topics(pagination.items)

        self.render('node/show_node.html', node=node, pagination=pagination)



class CreateNodeTopicHandler(UserHandler):
    @require_user
    def get(self, node_name):
        node = Node.query.get_first(name=node_name)
        if node.platform != 0:
            return self.send_error(403)
        topic = Topic()
        if not node:
            self.send_error(404)
            return
        self.render('topic/create_topic.html', node=node, topic=topic)

    @require_user
    def post(self, node_name):
        node = Node.query.get_first(name=node_name)
        if not node:
            self.send_error(404)
            return
        if node.platform != 0:
            return self.send_error(403)
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        hidden =  self.get_argument('hidden', None)
        topic = Topic()
        if not title:
            self.flash_message('Please fill the title field', 'error')
            self.render('topic/create_topic.html', node=node, topic=topic)
            return
        
        #: avoid double submit
         
        digest = hashlib.md5(utf8(title)).hexdigest()
        key = "t:p%d:%s" % (self.current_user.id, digest)
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
        topic.people_id = self.current_user.id
        topic.hidden = hidden
        node.topic_count += 1
        db.session.add(topic)
        db.session.add(node)
        db.session.commit()

        url = '/topic/%d' % topic.id
        autocache_set(key, url, 100)
        self.redirect(url)

        #: notification
        refer = '<a href="/topic/%s">%s</a>' % (topic.id, topic.title)
        for username in set(find_mention(title)):
            self.create_notification(username, title, refer,
                                     exception=topic.people_id)
        for username in set(find_mention(content)):
            self.create_notification(username, content, refer,
                                     exception=topic.people_id)

        #TODO social networks


class ShowAllNodesHandler(UserHandler):

    def get(self):
        nodes = Node.query.filter_by(platform=0).order_by('-last_updated').all()
        self.render('node/node_list.html', nodes=nodes)

  

app_handlers = [
    url('', ShowAllNodesHandler, name='show-all-nodes'),
    url('/new', CreateNodeHandler, name='new-node'),
    url('/([a-z0-9]+)', ShowNodeHandler, name='show-node'),
    url('/([a-z0-9]+)/new', CreateNodeTopicHandler, name='new-node-topic'),
    ('/(\w+)/follow', FollowNodeHandler),
    ('/(\w+)/edit', EditNodeHandler),

]


class NodeModule(UIModule):
    def render(self, node):
        user = self.handler.current_user
        if not user:
            following = False
        elif FollowNode.query.get_first(people_id=user.id, node_id=node.id):
            following = True
        else:
            following = False

        return self.render_string('module/node.html', node=node,
                                  following=following)


class FollowingNodesModule(UIModule):
    def render(self, people_id):
        fs = FollowNode.query.filter_by(people_id=people_id).values('node_id')
        node_ids = (f[0] for f in fs)
        nodes = Node.query.filter_by(id__in=node_ids).all()
        return self.render_string('module/show_node_list.html', nodes=nodes)


class RecentAddNodesModule(UIModule):
    def render(self):
        nodes = Node.query.filter_by(platform=0).order_by('-id')[:20]
        return self.render_string('module/show_node_list.html', nodes=nodes)

class RecentNodesModule(UIModule):
    def render(self):
        nodes = Node.query.filter_by(platform=0).order_by('-id')[:20]
        return self.render_string('node/recent_nodes.html', nodes=nodes)


app_modules = {
    'Node': NodeModule,
    'FollowingNodes': FollowingNodesModule,
    'RecentAddNodes': RecentAddNodesModule,
    'RecentNodes':RecentNodesModule
}

app = DojangApp('node', __name__, handlers=app_handlers, ui_modules=app_modules)
