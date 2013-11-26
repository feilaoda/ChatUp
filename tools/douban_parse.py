# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import os
import sys
import urllib2
import re
import json

from urlparse import urljoin
import MySQLdb as mdb
from time import sleep
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
import md5
import logging
import threading
import string
import types

logger = logging.getLogger(__name__)


douban_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        #'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',
        'Cookie': 'bid="fpxA/+U9YOg"; ll="0"; dbcl2="43119928:wi3TvNqdmIY"; ck="oCad"; __utma=30149280.1155395163.1365728926.1365759320.1365847560.6; __utmb=30149280.7.10.1365847560; __utmc=30149280; __utmz=30149280.1365847560.6.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.4311'
        }


def create_request(url, headers):
    request = urllib2.Request(url)
    for k,v in headers.items():
        request.add_header(k, v)
    return request

def parse_url(result):
    if result['code'] != 200:
        return [],[]
    html = result['html']
    hxs = HtmlXPathSelector(text=html)
    links = hxs.select('//a/@href').extract()
    new_urls = []
    for url in links:
        if re.search(r'http://movie.douban.com/subject/\d+', url):
            new_urls.append(url)

    return new_urls

def fetch_url(url):
    logger.debug("Download starting...\n[%s]" % url)


    request = create_request(url, douban_headers)
    try:
        response = urllib2.urlopen(request, timeout=20)
        html = response.read()
        if ('Content-Encoding' in response.headers and response.headers['Content-Encoding']) or \
                ('content-encoding' in response.headers and response.headers['content-encoding']):
                import gzip
                import StringIO
                data = StringIO.StringIO(html)
                gz = gzip.GzipFile(fileobj=data)
                html = gz.read()
                gz.close()

        if 'Set-Cookie' in response.headers:
            cookies = response.headers['Set-Cookie']
            douban_headers['Cookie'] = cookies

        response.close()
        logger.debug("Download end\n[%s]" % url)
        return dict(code=200, url=url, html=html)

    except urllib2.HTTPError, e:
        print 'you got an error with the code', e
        return dict(code = e.code)
    except urllib2.URLError, e:
        print 'you got an error with the code', e
        return dict(code = 500)

    return dict(code=-1)

 

def main():
    urls = ["http://movie.douban.com/top250?format=text",]
    for url in urls:
        res = fetch_url(url)
        links = parse_url(res)
        for link in links:
            print link

if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf8') 
    main()
