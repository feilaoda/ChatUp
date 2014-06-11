# -*- coding: utf-8 -*-

debug = True
#address = '0.0.0.0'
sqlalchemy_engine = "mysql://root:admin@localhost:3306/space2x?charset=utf8"
port=80
version="1.0"

autoescape=None
login_url = "/account/signin"

# memcache = "127.0.0.1:11211"
cookie_secret = "space2x.com 3fd0348db6303181634291f252fb9172"
password_secret = "3fd0348db6303181634291f252fb9172"
static_url_prefix = '/static/'

cookie_domain=".space2x.com"
default_domain="www.space2x.com"
image_domain = "http://www.space2x.com"
api_domain = "api.space2x.com"
static_domain = "http://www.space2x.com"

api_version = "v1"
api_url="http://api.space2x.com/"+api_version
api_secret = "testkey"

sitename = "space(2x)"
site_url = "http://www.space2x.com"
site_cache_prefix = "cu:"
static_path = "app/static"
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

github_key = 'testkey'
github_secret = 'testsecret'
github_redirect_uri = 'http://www.space2x.com/account/callback/github'

douban_key = 'testkey'
douban_secret = 'testsecret'

weibo_key = 'testkey'
weibo_secret = 'testsecret'

local_upload_path = 'e:/source/python/keepcd/static/upload'
local_upload_url = '/static/upload'
local_image_path = '/Users/feilaoda/Documents/project/ChatUp/app'
local_media_path = '/Users/feilaoda/Documents/project/ChatUp/app'

static_avatar_default = 'http://www.space2x.com/static/assets/images/profile.png'
static_avatar_path = '/Users/feilaoda/Documents/project/ChatUp/app/static/avatar'
static_avatar_url = 'http://www.space2x.com/static/avatar'

default_locale = 'zh_CN'
#: smtp
smtp_user = 'noreply@gmail.com'
smtp_password = 'password'
smtp_host = 'smtp.gmail.com'
smtp_ssl = True
mobile_ua_ignores = []
redis_clients = { 'host': '127.0.0.1', 'port': 6379}

