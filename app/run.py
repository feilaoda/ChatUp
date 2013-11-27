# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys
import formencode
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

from tornado.options import options
from dojang.util import reset_option
from dojang.app import DojangApplication
from dojang.web import init_options, run_server
from tornado.escape import xhtml_escape

# reset_option('debug', True, type=bool)
# reset_option('autoescape', None)
# reset_option('login_url', '/account/signin', type=str)
reset_option('template_path', os.path.join(PROJDIR, "templates/chatup"))
reset_option('locale_path', os.path.join(PROJDIR, 'locale'))
#reset_option('default_locale', 'zh-CN', type=str)
# # # site config
 
# # reset_option('sitefeed', '/feed')

# reset_option('static_path', os.path.join(PROJDIR, 'static'))
# reset_option('static_url_prefix', '/static/', type=str)


# reset_option('mobile_ua_ignores', [], type=list)
# reset_option('search_ua_strings', [], type=list)
# # factor config
# # reset_option('reply_factor_for_topic', 600, type=int)
# # reset_option('reply_time_factor', 1000, type=int)
# # reset_option('up_factor_for_topic', 1500, type=int)
# # reset_option('up_factor_for_user', 1, type=int)
# # reset_option('down_factor_for_topic', 800, type=int)
# # reset_option('down_factor_for_user', 1, type=int)
# # reset_option('accept_reply_factor_for_user', 1, type=int)
# # reset_option('up_max_for_user', 10, type=int)
# # reset_option('down_max_for_user', 4, type=int)
# # reset_option('vote_max_for_user', 4, type=int)
# # reset_option('promote_topic_cost', 100, type=int)

# # third party support config
# reset_option('gravatar_base_url', "http://www.gravatar.com/avatar/")
# reset_option('gravatar_extra', '')
# reset_option('recaptcha_key', '')
# reset_option('recaptcha_secret', '')
# reset_option('recaptcha_theme', 'clean')
# reset_option('emoji_url', '')

# # image backend
# # reset_option('image_backend', 'app.front.backends.LocalBackend')
# reset_option('redis_clients', {}, type=dict)


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
    
    application.register_app('app.admin.channel.handlers.app')
    application.register_app('app.admin.people.handlers.app')
    application.register_app('app.admin.topic.handlers.app')
    application.register_app('app.admin.handlers.app')


    application.register_app('app.about.handlers.app')

    
    


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




    from app.lib.util import xmldatetime,xmlday, localtime, timesince, linkto
    from app.lib.urls import topic_url, build_url, build_image_url
    from app.lib.filters import markup
    from dojang.escape import simple_escape, html_escape, br_escape
    from urllib import urlencode
    from tornado import locale

    default_locale = locale.get('zh-CN')
    application.register_filter('locale', default_locale)
    # application.register_filter('markdown', markdown)
    application.register_filter('markup', markup)
    
    # application.register_filter('normal_markdown', normal_markdown)
    application.register_filter('xmldatetime', xmldatetime)
    
    application.register_filter('xmlday', xmlday)
    application.register_filter('localtime', localtime)
    application.register_filter('timesince', timesince)
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

    sys.setdefaultencoding('utf8') 
    init_options()
    # init_caches()
    application = create_application()
    run_server(application)


if __name__ == "__main__":
    main()
