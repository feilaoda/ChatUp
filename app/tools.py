#!/usr/bin/env python

import argparse
import urllib2
import json
from dojang.util import parse_config_file, create_token
from tornado.options import options 
import os
PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    import app
    print('Start keepcd version: %s' % app.__version__)
except ImportError:
    import site
    site.addsitedir(ROOTDIR)
    print PROJDIR
    print('Development of keepcd')

def create_db():
    from dojang.database import db
    # import account.models
    # import note.models
    # import entity.models
    
    # import board.models
    # import pin.models
    # import readlist.models
    # import movie.models
    # import tag.models
    # import search.models
    # import node.models
    # import topic.models
    # import english.models
    # import sound.models
    # import blog.models
    # import food.models
    import todo.models

    # from account.models import Weibo

    print "create_db"
    db.Model.metadata.create_all(db.engine)
    return

def reset_entity_salt():
    from dojang.database import db
    from app.entity.models import Entity
    from app.account.models import People
    from app.movie.models import Movie, PeopleAddedLink,MovieMediaLink, MediaLink,MediaLinkHash, MovieImage, MovieTag, MovieWatchList

    entities  = Entity.query.filter_by().all()
    print "entities ", len(entities)
    for e in entities:
        e.salt = create_token(32).upper()
        db.session.add(e)
        db.session.commit()


def fetch_rss_app(url, refetch='false'):
    link = ''
    res = []
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1')
        response = urllib2.urlopen(request,  timeout=100)
        data = response.read()
        apps = json.loads(data, encoding='utf-8')
        
        errors = dict()
        
        count = 0
        
        for app in apps['feed']['entry']:
            print app['im:name']['label'], "\t\t\t",app['id']['label']
            link = app['id']['label']


            api_link = '%s/appstore/fetch?refetch=%s&url=%s&format=json' % (options.siteurl, refetch, link)
            req = urllib2.Request(api_link)
            urllib_res = urllib2.urlopen(req,  timeout=30)
            response = urllib_res.read()
            if response != 'ok':
                print link, response

        
    except Exception, error:
        #raise error
        return dict(result=str(error), link=link)
       
    return dict(result='ok')

def create_superuser():
    from july.database import db
    from account.models import Member
    cmd = raw_input('Create superuser?(Y/n): ')
    if cmd == 'n':
        import sys
        sys.exit(1)
    import getpass
    username = raw_input('username: ')
    email = raw_input('email: ')
    password = getpass.getpass('password: ')
    user = Member(email=email, username=username)
    user.password = Member.create_password(password)
    user.role = 10
    db.session.add(user)
    db.session.commit()
    return user

def test_upload_weibo_pic():
    from weibo import APIClient
    import webbrowser
    client = APIClient(app_key=options.weibo_key, app_secret=options.weibo_secret,
                   redirect_uri="http://test.keepcd.com/account/weibo/auth")
    #url = client.get_authorize_url()
    #print url
    #webbrowser.open(url)
    code = '935f1dc18844b0b0cb483c49b596c75f'
    #r = client.request_access_token(code)
    access_token = '2.00_k8AtBhkxLAC55ccefabbcuMzpPE' #r.access_token
    expires_in = '157679999' #r.expires_in
    print access_token, expires_in
    client.set_access_token(access_token, expires_in)
    f = open('d:/noname.jpg', 'rb')
    # r = client.statuses.update.post(status=u'test weibo python')
    r = client.statuses.upload.post(status=u'test weibo with picture', pic=f)
    f.close() 
    print r

config = '''debug = False
master = "sqlite:////tmp/june.sqlite"
memcache = "127.0.0.1:11211"
cookie_secret = "cookiesecret"
password_secret = "passwordsecret"

sitename = "June"
siteurl = "http://python-china.org"

recaptcha_key = ''
recaptcha_secret = ''
'''


def init_project():
    f = open('settings.py', 'w')
    f.write(config)
    f.close()
    return


def main():
    parser = argparse.ArgumentParser(
        prog='june',
        description='June: a forum',
    )
    parser.add_argument('command', nargs="*")
    parser.add_argument('-f', '--settings', dest='config')
    args = parser.parse_args()

    if args.config:
        parse_config_file(args.config)  # config
    else:
        return init_project()

    def run_command(cmd):
        if cmd == 'createdb':
            return create_db()
        if cmd == 'createuser':
            return create_superuser()
        if cmd == 'init':
            return init_project()
        if cmd == 'salt':
            return reset_entity_salt()
        if cmd == 'fetchapp':
            #top paid games app
            print 'fetchapp'
            print fetch_rss_app('http://itunes.apple.com/us/rss/toppaidapplications/limit=300/genre=6014/json')

        if cmd == 'weibo':
            return test_upload_weibo_pic()

        if cmd == 'test':
            from dojang.cache import complex_cache, get_cache_list
            from account.models import People
            import cPickle
            # ps = People.query.all()
            user_list = dict()
            # for p in ps:
            #    user_list[p.id] = cPickle.dumps(p)
            # complex_cache.hmset('people', user_list)

            # res = complex_cache.hmget('people', user_list.keys())
            #id_list = user_list.keys()
            # id_list = complex_cache.hkeys('people')
            # data = complex_cache.hmget('people', id_list)
            # user_list.clear()
            # data_ids = []
            # for d in data:
            #     d = cPickle.loads(d)
            #     user_list[p.id] = p
            #     data_ids.append(str(p.id))
            # missing = set(id_list) - set(data_ids)
            # print "missing",set(id_list),set(data_ids), missing
            # if missing:
            #     print "set missing"
            #     dct = {}
            #     for item in People.query.filter_by(id__in=missing).all():
            #         dct[item.id] = item
            #     complex_cache.hmset('people', dct)
            #     data.update(dct)

            data = get_cache_list(People, [], 'people')

            #res = get_cache_list(People, user_list.keys(), 'people:')
            for d in data:
                print "data", d, type(d)

    if isinstance(args.command, basestring):
        return run_command(args.command)
    if isinstance(args.command, (list, tuple)):
        for cmd in args.command:
            run_command(cmd)


if __name__ == "__main__":
    main()
