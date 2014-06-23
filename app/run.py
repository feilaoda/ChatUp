# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys

from dojang.app import DojangApplication
from dojang.util import reset_option
from dojang.web import init_options, run_server
import formencode
from tornado.escape import xhtml_escape
from tornado.options import options
import logging

# import jieba
# jieba.load_userdict("userdict.txt")
PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    #
    import site
    site.addsitedir(ROOTDIR)
    import app
    print PROJDIR
    print('Start chatup version: %s' % app.__version__)
except ImportError:
    print('Development of chatup')


reset_option('template_path', os.path.join(PROJDIR, "templates/v3"))
reset_option('locale_path', os.path.join(PROJDIR, 'locale'))


def create_application():
    formencode.api.set_stdtranslation(languages=["en_US"])

    settings = dict(
        debug=options['debug'],
        autoescape=options.autoescape,
        cookie_secret=options.cookie_secret,
        xsrf_cookies=True,
        login_url=options.login_url,

        template_path=options.template_path,
        static_path=options.static_path,
        static_url_prefix=options.static_url_prefix,
    )
    #: init application

    application = DojangApplication(**settings)

    application.register_app('app.account.handlers.app')
    application.register_app('app.people.handlers.app')
    application.register_app('app.node.handlers.app')
    application.register_app('app.topic.handlers.app')
    application.register_app('app.group.handlers.app')

    application.register_app('app.wist.handlers.app')


    # application.register_app('app.admin.channel.handlers.app')
    application.register_app('app.admin.people.handlers.app')
    application.register_app('app.admin.topic.handlers.app')
    application.register_app('app.admin.handlers.app')

    application.register_app('app.about.handlers.app')

    # application.register_app('app.wepusher.handlers.app')
    # application.register_api('app.wepusher.api.app', options.api_domain)
    # application.register_api('app.wepusher.api.wepusher_app', options.wepusher_api_domain)

    #http://www.xxx.com/api/v1/account/xxx
    application.register_api('app.account.api.app', options.api_domain)

    #http://api.xxx.com/v1/people/xxx
    application.register_api('app.people.api.app', options.api_domain)

    #http://api.xxx.com/v1/topic/xxx
    application.register_api('app.topic.api.app', options.api_domain)


    application.register_app('app.front.handlers.app')

    for key in ['sitename', 'site_url', 'sitefeed', 'version', 'ga', 'gcse']:
        application.register_context(key, options[key])


    import datetime
    application.register_context('now', datetime.datetime.utcnow)




    from app.lib.util import xmldatetime,xmlday, localtime, timesince, linkto, seconds_since
    from app.lib.urls import topic_url, build_url, build_image_url
    from app.lib.filters import markup, markdown
    from dojang.escape import simple_escape, html_escape, br_escape
    from urllib import urlencode
    from tornado import locale

    default_locale = locale.get('zh-CN')
    application.register_filter('locale', default_locale)
    application.register_filter('markdown', markdown)
    application.register_filter('markup', markup)

    # application.register_filter('normal_markdown', normal_markdown)
    application.register_filter('xmldatetime', xmldatetime)

    application.register_filter('xmlday', xmlday)
    application.register_filter('localtime', localtime)
    application.register_filter('timesince', timesince)

    application.register_filter('seconds_since', seconds_since)
    application.register_filter('topic_url', topic_url)

    application.register_filter('url_encode', urlencode)
    application.register_filter('url', build_url)
    application.register_filter('image_url', build_image_url)
    # application.register_filter('movie_filter_url', movie_filter_url)
    application.register_filter('linkto', linkto)
    application.register_filter('simple_escape', simple_escape)
    application.register_filter('br_escape', br_escape)
    application.register_filter('html_escape', html_escape)



    return application


def main():
    reload(sys)
    # logger.setLevel(logging.DEBUG)
    sys.setdefaultencoding('utf8')
    init_options()
    application = create_application()
    run_server(application)


if __name__ == "__main__":
    main()
