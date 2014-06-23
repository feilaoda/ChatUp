# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys

import formencode


PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    # 
    import site
    site.addsitedir(ROOTDIR)
    import keepcd
    print PROJDIR
    print('Start meiban version: %s' % keepcd.__version__)
except ImportError:
    print('Development of meiban')



# print "user"
# print validators.username("??????3")
# print validators.nickname(u'????????????')



git_url = 'https://api.github.com/user?access_token=2d615d332926a712775057c3a95b9cd72793fab6&fields=login'

from tornado import httpclient
import urllib

def github_request(path, callback, access_token=None,
                           post_args=None, **args):
    url = "https://api.github.com" + path
    all_args = {}
    if access_token:
        all_args["access_token"] = access_token
        all_args.update(args)
        all_args.update(post_args or {})
    if all_args:
        url += "?" + urllib.urlencode(all_args)
    http = httpclient.AsyncHTTPClient()
    if post_args is not None:
        http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                   callback=callback)
    else:
        http.fetch(url, callback=callback)

def _on_github_request(callback, response):
    if response.error:
        logging.warning("Error response %s fetching %s", response.error,
                        response.request.url)
    print response.request.url


github_request('/user', callback=_on_github_request, access_token='2d615d332926a712775057c3a95b9cd72793fab6')

