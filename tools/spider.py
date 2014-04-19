# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import json
import os
import re
import sys
import urllib
import urllib2

from dojang.util import parse_config_file
from tornado.options import options


PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    import keepcd
    print('Start keepcd version: %s' % keepcd.__version__)
except ImportError:
    import site
    site.addsitedir(ROOTDIR)
    site.addsitedir(ROOTDIR+"/keepcd")
    print('Development of keepcd: ' + ROOTDIR)



def spider_callback(self, message):
    print message


def run_command(name, second_arg):
    if name == 'dl_eslpod':
        download_eslmp3()
    elif name == "parse_elspod":
        parse_eslmp3()
    else:
        from dojang.util import parse_config_file, import_object
        from easycrawl.models import CrawlSite

        # from keepcd.admin.easycrawl.douban.app import worker
        site = CrawlSite.query.filter_by(name=name).first()
        worker_name = "easycrawl.%s.app.worker" % name
        print worker_name
        worker = import_object(worker_name)
        if second_arg == 'debug':
            print "\nexec debug()\n\n"
            worker.debug()
            worker.finished()
        elif second_arg == 'parse':
            print "\nexec parse()\n\n"
            worker.parse()
        else:
            print "\nexec run()\n\n"
            worker.run()
            worker.finished()


def download_file(url, filename):
    try:
        u = urllib.FancyURLopener()
        u.retrieve(url, filename)
    except IOError as e:
        url = u.headers['Location']
        print e
        print url
        


def download_eslmp3():
    from easycrawl.eslpod.models import EslPod
    pods = EslPod.query.filter_by().all()
    for pod in pods:
        if pod.media:
            media = pod.media
            media_file = media.split('/')
            mp3_file = media_file[-1]
            dest_file = "/Users/zhenng/tmp/eslpod/" + mp3_file 
            if not os.path.exists(dest_file):
                print media
                download_file(media, dest_file)

def parse_eslmp3():
    from easycrawl.eslpod.models import EslPod
    pods = EslPod.query.filter_by().all()
    for pod in pods:
        if pod.media:
            media = pod.media
            media_file = media.split('/')
            mp3_file = media_file[-1]
            mp3_filename = mp3_file.split('.')[0]
            src_file = "/Users/zhenng/tmp/eslpod/old/" + mp3_file
            dest_file = "normal/" + mp3_filename
            #print pod.fast_dialog
            if not os.path.exists(src_file):
                #print "not exists", src_file
                continue

            if pod.fast_dialog:
                fast_time = pod.fast_dialog
                #print "fasttime: type", type(fast_time)
                fast_time = fast_time.replace(":", ".")
                cmd = "mp3splt -o %s %s %s EOF-0.30" % (dest_file, src_file, fast_time)
                print cmd
                os.system(cmd)



if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf8') 
    parser = argparse.ArgumentParser(
        prog='keep cd',
        description='keep',
    )
    parser.add_argument('command', nargs="*")
    args = parser.parse_args()

    name = args.command[0]

    second_arg = None
    if len(args.command) >= 2:
        second_arg = args.command[1]
        
    parse_config_file("../settings.py")
    

    run_command(name, second_arg)
    # r = "^/movies/\d+[/]*$ || http://imax.im/movies/\d+[/]*$"
    # # r = "^http://movie.douban.com/subject/\d+[/]*$"
    # url = 'http://imax.im/movies/36172'
    # # url = 'http://movie.douban.com/subject/2345'
    # ps = r.split('||')
    # for patten in ps:
    #     patten = patten.strip()
    #     print patten
    #     if re.search(patten, url):
    #         print "true", url
    #     else:
    #         print "false", url

    
    
   	


