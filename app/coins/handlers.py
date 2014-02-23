# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib
import threading

from dojang.app import DojangApp
import tornado
from tornado.escape import utf8
from tornado.options import options
from tornado.web import UIModule, authenticated, RequestHandler
from tornado.web import URLSpec as url
from tornado.websocket import WebSocketHandler
import tornadoredis


# class OpenChannel(threading.Thread):
#     def __init__(self, channel, host = None, port = None):
#         threading.Thread.__init__(self)
#         self.lock = threading.Lock()
#         self.redis = redis.StrictRedis(host = host or 'localhost', port = port or 6379)
#         self.pubsub = self.redis.pubsub()
#         self.pubsub.subscribe(channel)
#         self.output = []
#     # lets implement basic getter methods on self.output, so you can access it like a regular list
#     def __getitem__(self, item):
#         with self.lock:
#             return self.output[item]
#     def __getslice__(self, start, stop = None, step = None):
#         with self.lock:
#             return self.output[start:stop:step]
#     def __str__(self):
#         with self.lock:
#             return self.output.__str__()
#     # thread loop
#     def run(self):
#         for message in self.pubsub.listen():
#             with self.lock:
#                 self.output.append(message['data'])
#     def stop(self):
#         self._Thread__stop()
# # add a method to the application that will return existing channels
# # or create non-existing ones and then return them
# class ChannelMixin(object):
#     def GetChannel(self, channel, host = None, port = None):
#         if channel not in self.application.channels:
#             self.application.channels[channel] = OpenChannel(channel, host, port)
#             self.application.channels[channel].start()
#         return self.application.channels[channel]
# class ReadChannel(tornado.web.RequestHandler, ChannelMixin):
#     @tornado.web.asynchronous
#     def get(self, channel):
#         # get the channel
#         channel = self.GetChannel(channel)
#         # write out its entire contents as a list
#         self.write('{}'.format(channel[:]))
#         self.finish() # not necessary?
class OkCoinLtcHandler(RequestHandler):
    def get(self):
        self.render("coins/finance_charts.html", title="coin charts")

tc = tornadoredis.Client()
tc.connect()

class OkCoinLtcWebSocketHandler(WebSocketHandler):
    def __init__(self,  *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client()
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, "okcoin_ltc")
        self.client.listen(self.on_message)

    def on_message(self, msg):
        if msg.kind == 'message':
            self.write_message(str(msg.body))
        if msg.kind == 'disconnect':
            # Do not try to reconnect, just send a message back
            # to the client and close the client connection
            self.write_message('The connection terminated '
                               'due to a Redis server error.')
            self.close()

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe("okcoin_ltc")
            self.client.disconnect()


class NewMessageHandler(tornado.web.RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        message = self.get_argument('message')
        tc.publish('okcoin_ltc', message)
        self.set_header('Content-Type', 'text/plain')
        self.write('sent: %s' % (message,))

app_handlers = [
    ('/okcoin/ltc', OkCoinLtcHandler),
    ('/websocket', OkCoinLtcWebSocketHandler),
    ('/msg', NewMessageHandler)
]

app_modules = {
}

app = DojangApp(
    'coins', __name__, handlers=app_handlers, ui_modules=app_modules,
)





