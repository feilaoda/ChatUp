# -*- coding: utf-8 -*-

debug = True
address = '0.0.0.0'
sqlalchemy_engine = "mysql://root:admin@localhost:3306/wecoders?charset=utf8"
port=80
version="1.0"

autoescape=None
login_url = "/account/signin"

# memcache = "127.0.0.1:11211"
cookie_secret = "wcs.com"
password_secret = "3fd0348db6303181634291f252fb9172"
static_url_prefix = '/static/'

cookie_domain=".wcs.com"
default_domain="www.wcs.com"
image_domain = "http://www.wcs.io"
api_domain = "api.wcs.com"
static_domain = "http://www.wcs.com"

api_version = "v1"
api_url="http://api.wcs.com/"+api_version
api_secret = "testkey"

sitename = "WeCoders"
site_url = "http://www.wcs.com"
site_cache_prefix = "wcs:"
static_path = "static"
sitefeed = ""

#: google analytics
ga = ""
gcse = ""
#: register your recaptcha at www.google.com/recaptcha
#: this is a public key
recaptcha_key = 'testkey'
recaptcha_secret = 'testsecret'
recaptcha_theme = 'clean'
#: if you have a gravatar proxy
#gravatar_base_url = ''
#gravatar_extra = ''

emoji_url = 'http://python-china.b0.upaiyun.com/emojis/'

#twitter_key = ''
#twitter_secret = ''

github_key = '9ae3c03f1708f6344b35'
github_secret = '643c94f04172ac2504832e71089f402d67316e33'
github_redirect_uri = 'http://www.wcs.com/account/callback/github'

douban_key = 'testkey'
douban_secret = 'testsecret'

weibo_key = 'testkey'
weibo_secret = 'testsecret'

local_upload_path = 'e:/source/python/keepcd/static/upload'
local_upload_url = '/static/upload'
local_image_path = '/Users/feilaoda/Work/Project/ChatUp/app'
local_media_path = '/Users/feilaoda/Work/Project/ChatUp/app'

static_avatar_default = 'http://www.wcs.com/static/assets/images/profile.png'
static_avatar_path = '/Users/feilaoda/Work/Project/ChatUp/static/avatar'
static_avatar_url = 'http://www.wcs.com/static/avatar'

default_locale = 'zh_CN'
#: smtp
smtp_user = 'noreply@gmail.com'
smtp_password = 'password'
smtp_host = 'smtp.gmail.com'
smtp_ssl = True
mobile_ua_ignores = []
redis_clients = { 'host': '127.0.0.1', 'port': 6379}
