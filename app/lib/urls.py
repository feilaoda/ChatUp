import datetime
import re
import urllib2

from tornado.options import options
from util import join_list, to_md5


def build_url(name, id=None, kwargs=None):
    if name is None:
        return ''
    names = name.split(':')
    module = names[0]
    path = names[1]
    if id:
        return '/%s/%s' % (module, id)
    for k,v in kwargs:
        return '/%s/%s' % (module, v)


def build_image_url(url):
    if not url:
        return ""
    if url.find('http://') >= 0:
        return url
    else:
        return options.image_domain + url


def topic_url(topic, perpage=30):
    url = '/topic/%s' % topic.id
    num = (topic.reply_count - 1) / perpage + 1
    if not topic.reply_count:
        return url
    if num > 1:
        url += '?p=%s' % num

    url += '#reply%s' % topic.reply_count
    return url

