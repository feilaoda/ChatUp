import hashlib
import os.path

from app.account.decorators import require_user
from app.account.lib import UserHandler
from app.account.models import People
from app.channel.models import Channel, ChannelEntry
from app.topic.lib import get_full_topics
from app.topic.models import Topic
from app.node.models import Node

from dojang.app import DojangApp
from dojang.cache import autocached
from dojang.util import import_object
from dojang.web import DojangHandler
from tornado.options import options
from tornado.web import RequestHandler
from tornado.web import UIModule



class FrontHandler(UserHandler):
    def get(self):
        p = self.get_argument('p', 1)
        limit = 30
        nodes = Node.query.filter_by().all()
        node_ids = []
        for node in nodes:
            node_ids.append(node.id)
        pagination = Topic.query.filter(Topic.node_id.in_(node_ids)).order_by('-last_reply_time').paginate(p, limit)

        pagination.items = get_full_topics(pagination.items)

        self.render('front/index.html', pagination=pagination)



class LinkToHandler(DojangHandler):
    def get(self):
        url = self.get_argument('url', None)
        if not url:
            self.send_error(404)
            return
        self.redirect('%s' % (url))


handlers = [
    ('/', FrontHandler),
    ('/linkto', LinkToHandler),
]

class ShowFrontTopicChannelsModule(UIModule):
    def render(self):
        topic_channels = Channel.query.filter_by(isa='topic').order_by('sorting').all()
        return self.render_string('front/front_topic_channels.html', topic_channels=topic_channels)


class ShowFrontTopicChannelModule(UIModule):
    def render(self, channel):
        entries = channel.entries
        return self.render_string('front/front_topic_channel_module.html', channel=channel, entries=entries)

class ShowFrontTopicsSidebarModule(UIModule):
    def render(self):
        topics = Topic.query.filter_by().order_by('-created').limit(10).all()
        return self.render_string('front/front_topics_sidebar.html', topics=topics)

class ShowFrontRecentTopicsModule(UIModule):
    def render(self):

        # topics = Topic.query.filter_by().order_by('-last_reply_time').limit(20).all()
        # topics = get_full_topics(topics)
        return self.render_string('front/front_recent_topics.html', pagination=pagination)


app_modules = {
    'ShowFrontTopicChannels': ShowFrontTopicChannelsModule,
    'ShowFrontTopicChannel': ShowFrontTopicChannelModule,
    'ShowFrontTopicsSidebar': ShowFrontTopicsSidebarModule,
    'ShowFrontRecentTopics': ShowFrontRecentTopicsModule
}



app = DojangApp('', __name__, handlers=handlers, ui_modules=app_modules,)













 # ('/following', FollowingHandler),
    # ('/popular', PopularHandler),
    # ('/preview', PreviewHandler),
    # ('/feed', SiteFeedHandler),
    # ('/search', SearchHandler),
    # ('/upload', UploadHandler),
    # ('/node/(\w+)', NodeHandler),
    # ('/node/(\w+)/feed', NodeFeedHandler),
    # ('/member/(\w+)', MemberHandler),
    # ('/~(\w+)', RedirectMemberHandler),
    # ('/doc/(\w+)', DocHandler),



# class LatestHandler(UserHandler):
#     def head(self):
#         pass

#     def get(self):
#         title = 'Latest'

#         p = self.get_argument('p', 1)
#         pagination = Topic.query.order_by('-last_reply_time').paginate(p, 30)

#         pagination.items = get_full_topics(pagination.items)

#         app_pagination = AppStore.query.paginate(1, 50)
#         box = AppBox.query.filter_by(name="topgames").first()
#         if box is not None:
#             items = AppBoxItem.query.filter_by(box_id=box.id).order_by('order_by').all()
#         else:
#             items = []

#         self.render('topic_list.html', title=title, pagination=pagination, items=items)


# class PopularHandler(UserHandler):
#     def head(self):
#         pass

#     def get(self):
#         title = 'Popular'

#         p = self.get_argument('p', 1)
#         pagination = Topic.query.order_by('-impact').paginate(p, 30)

#         pagination.items = get_full_topics(pagination.items)
#         self.render('topic_list.html', title=title, pagination=pagination, items=[])


# class FollowingHandler(UserHandler):
#     @tornado.web.authenticated
#     def get(self):
#         title = 'Following'

#         user_id = self.current_user.id
#         fs = FollowNode.query.filter_by(user_id=user_id).values('node_id')
#         node_ids = (f[0] for f in fs)

#         p = self.get_argument('p', 1)
#         pagination = Topic.query.filter_by(node_id__in=node_ids)\
#                 .order_by('-last_reply_time').paginate(p, 30)

#         pagination.items = get_full_topics(pagination.items)
#         self.render('topic_list.html', title=title, pagination=pagination, items=[])


# class NodeHandler(UserHandler):
#     def head(self, slug):
#         pass

#     def get(self, slug):
#         node = Node.query.filter_by(slug=slug).first_or_404()

#         p = self.get_argument('p', 1)
#         pagination = Topic.query.filter_by(node_id=node.id)\
#                 .order_by('-impact').paginate(p, 30)

#         pagination.items = get_full_topics(pagination.items)
#         self.render('node.html', node=node, pagination=pagination)


# class MemberHandler(UserHandler):
#     def get(self, username):
#         user = Member.query.filter_by(username=username).first_or_404()

#         q = Topic.query.filter_by(user_id=user.id)
#         topics = get_full_topics(q.order_by('-id')[:10])

#         #: user's faved topics {{{
#         #: TODO cache
#         votes = Vote.query.filter_by(user_id=user.id, type='up')\
#                 .values('topic_id')
#         topic_ids = (v[0] for v in votes)
#         q = Topic.query.filter_by(id__in=topic_ids)
#         likes = get_full_topics(q.order_by('-id')[:10])
#         #: }}}

#         replies = Reply.query.filter_by(user_id=user.id).order_by('-id')[:20]
#         self.render('member.html', topics=topics, likes=likes, user=user,
#                     replies=replies)


# class RedirectMemberHandler(JulyHandler):
#     def get(self, username):
#         self.redirect('/member/%s' % username)


# class SiteFeedHandler(JulyHandler):
#     def get_template_path(self):
#         return os.path.join(os.path.dirname(__file__), '_templates')

#     def get(self):
#         self.set_header('Content-Type', 'text/xml; charset=utf-8')
#         html = cache.get('sitefeed')
#         if html is not None:
#             self.write(html)
#             return
#         topics = get_full_topics(Topic.query.order_by('-id')[:20])
#         html = self.render_string('feed.xml', topics=topics)
#         cache.set('sitefeed', html, 1800)
#         self.write(html)


# class NodeFeedHandler(JulyHandler):
#     def get_template_path(self):
#         return os.path.join(os.path.dirname(__file__), '_templates')

#     def get(self, slug):
#         node = Node.query.get_first(slug=slug)
#         if not node:
#             self.send_error(404)
#             return

#         self.set_header('Content-Type', 'text/xml; charset=utf-8')
#         key = 'nodefeed:%s' % str(slug)
#         html = cache.get(key)
#         if html is not None:
#             self.write(html)
#             return

#         topics = Topic.query.filter_by(node_id=node.id)[:20]
#         topics = get_full_topics(topics)
#         html = self.render_string('node_feed.xml', topics=topics, node=node)
#         cache.set(key, html, 1800)
#         self.write(html)


# class PreviewHandler(UserHandler):
#     def post(self):
#         text = self.get_argument('text', '')
#         self.write(markdown(text))


# class SearchHandler(UserHandler):
#     def get(self):
#         query = self.get_argument('q', '')
#         self.render('search.html', query=query)


# class DocHandler(UserHandler):
#     def get(self, slug):
#         doc = Document.query.filter_by(slug=slug).first_or_404()
#         self.render('doc.html', doc=doc)


# class UploadHandler(UserHandler):
#     @require_user
#     @tornado.web.asynchronous
#     def post(self):
#         image = self.request.files.get('image', None)
#         if not image:
#             self.write('{"stat": "fail", "msg": "no image"}')
#             self.finish()
#             return
#         image = image[0]
#         content_type = image.get('content_type', '')
#         if content_type not in ('image/png', 'image/jpeg'):
#             self.write('{"stat": "fail", "msg": "filetype not supported"}')
#             self.finish()
#             return
#         body = image.get('body', '')
#         filename = hashlib.md5(body).hexdigest()
#         if content_type == 'image/png':
#             filename += '.png'
#         else:
#             filename += '.jpg'

#         backend = import_object(options.image_backend)
#         backend.save(body, filename, self._on_post)

#     def _on_post(self, result):
#         if result:
#             self.write('{"stat":"ok", "url":"%s"}' % result)
#         else:
#             self.write('{"stat":"fail", "msg": "server error"}')
#         self.finish()
