# -*- coding: utf-8 -*-

import Image
import datetime
import errno
import md5
import os
from random import choice
import re
import stat
import urllib

import tornado
from tornado.escape import xhtml_escape
from watermark import watermark


chars = ('0123456789'
             'abcdefghijklmnopqrstuvwxyz'
             'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def find_mention(text):
    regex = r'@(\w+)\s'
    return re.findall(regex, text)


def force_int(num, default=1):
    try:
        return int(num)
    except:
        return default


def linkto(url, id=None):
    return '/linkto?url=%s&id=%d' % (url, id)

def create_token(length=16):
    salt = ''.join([choice(chars) for i in range(length)])
    return salt

def join_list(string, array):
    new_array = []
    for a in array:
        if a:
            new_array.append(a)
    return string.join(new_array)

def to_md5(url):
    m = md5.new()
    m.update(url)
    url_md5 = m.hexdigest()
    return url_md5 
    
def file_md5(name):
    m = md5.new()
    a_file = open(name, 'rb')    #?????????????????????????????????????????????
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

def join_or_merge_set(list1, list2):
    if list1 is None or len(list1) == 0:
        return list2
    if list2 is None or len(list2) == 0:
        return list1
    return set(list1) & set(list2)
    

def mkdir_p(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

def is_samefile(src, dst):
    # Macintosh, Unix.
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    # All other platforms: check for same pathname.
    return (os.path.normcase(os.path.abspath(src)) ==
            os.path.normcase(os.path.abspath(dst)))

def copyfileobj(fsrc, fdst, length=16*1024):
    """copy data from file-like object fsrc to file-like object fdst"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)

def copyfile(src, dst):
    """Copy data from src to dst"""
    if is_samefile(src, dst):
        raise Error("`%s` and `%s` are the same file" % (src, dst))

    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:
            # File most likely does not exist
            pass
        else:
            # XXX What about other special files? (sockets, devices...)
            if stat.S_ISFIFO(st.st_mode):
                raise SpecialFileError("`%s` is a named pipe" % fn)

    with open(src, 'rb') as fsrc:
        with open(dst, 'wb+') as fdst:
            copyfileobj(fsrc, fdst)


def xmldatetime(value):
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')

def xmlday(value):
    now = datetime.datetime.utcnow()
    delta = now - value
    if delta.days <= 0:
        return u"??????"
    elif delta.days <= 1:
        return u"??????"
    return value.strftime('%Y-%m-%d')


def localtime(value, timezone=8):
    value = value + datetime.timedelta(hours=timezone)
    return value.strftime('%Y-%m-%d %H:%M:%S')


def timesince(value, locale='en_US'):
    _ = tornado.locale.get(locale).translate
    now = datetime.datetime.utcnow()
    delta = now - value
    if delta.days > 365:
        return _('%s years ago') % (delta.days / 365)
    if delta.days > 30:
        return _('%s months ago') % (delta.days / 30)
    if delta.days > 0:
        return _('%s days ago') % delta.days
    if delta.seconds > 3600:
        return _('%s hours ago') % (delta.seconds / 3600)
    if delta.seconds > 60:
        return _('%s minutes ago') % (delta.seconds / 60)
    return _('just now')

def seconds_since(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    r = ""
    if h > 0:
        r += "%dh" % h
    if m > 0:
        r += "%2dm" % m
    if s >= 0:
        r += "%2ds" % s
    return r
    



def make_thumb(path, filename, size):
   
    base, ext = os.path.splitext(path)
    try:
        im = Image.open(path)
    except IOError:
        return
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # ??????????????????????????????
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')
            
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)            
        region = im.crop(box)
            
    #for size in sizes:
        #filename = base + "_" + "%sx%s" % (str(size), str(size)) + ".jpg"
    thumb = region.resize((size,size), Image.ANTIALIAS)
    thumb.save(filename, quality=100) # ?????? JPEG ??????????????? 75, ????????????????????????(0~100)


def make_resize(from_file, to_file, max_width, max_height):
    try:
        im = Image.open(from_file)
    except IOError:
        return

    width, height = im.size
 
    if im.mode != "RGB":
        im = im.convert("RGB")
    
    im = im.resize((max_width, max_height), Image.ANTIALIAS)
    #im.thumbnail((max_width,max_height),resample=1)
    im.save(to_file, quality=100)

def download_image(url, filename):
    image = urllib.URLopener()
    image.retrieve(url, filename)


def download_douban_image(douban_id, url, to_prefix):
    from_path = "/tmp/douban/%d.jpg" % (douban_id)
    try:
        mkdir_p(os.path.dirname(from_path))
        download_image(url, from_path)

        douban_str_id = str(douban_id)
        mid_path =  douban_str_id[-2:] + "/" + douban_str_id[-3:] 
       

        small_split_name = "small/" + mid_path + "/s" + douban_str_id + ".jpg"
        thumb_split_name = "small/" + mid_path + "/t" + douban_str_id + ".jpg"
        large_split_name = "large/" + mid_path + "/l" + douban_str_id + ".jpg"
        
        small_path = to_prefix + "/static/movies/" + small_split_name
        thumb_path = to_prefix + "/static/movies/" + thumb_split_name
        large_path = to_prefix + "/static/movies/" + large_split_name

        
        mkdir_p(os.path.dirname(thumb_path))
        mkdir_p(os.path.dirname(large_path))
        make_thumb(from_path, thumb_path , 75)
        make_resize(from_path, small_path, 150, 215)
        make_resize(from_path, large_path, 280, 400)
        # shutil.copyfile(from_path, large_path)
        # watermark(large_path,"static/assets/images/miniwater.png",'RIGHTTOP',opacity=0.7).save(large_path,quality=100)
        # watermark(large_path,"static/assets/images/water.png",'CENTERBOTTOM',opacity=0.5).save(large_path,quality=100)

        # watermark(small_path,"static/assets/images/miniwater.png",'CENTERTOP',opacity=0.2).save(small_path,quality=100)


        img_domain_prefix = "" #"http://www.keepcd.com"
        thumb_image = "/static/movies/"+ thumb_split_name;
        small_image = "/static/movies/"+ small_split_name;
        large_image = "/static/movies/"+ large_split_name;
        return True,thumb_image, small_image, large_image

    except Exception,e:
        print e
        return False, str(e),None,None



def parse_media_url(link_url):
    params = dict()
    category=''
    title=''
    size = 0
    hashes=dict()
    params['website'] = ''
    if link_url.startswith('ed2k://'):
        category, title, size, hashes = parse_ed2k_url(link_url)
    elif link_url.startswith('magnet:?'):
        category, title, hashes = parse_magnet_url(link_url)
    elif link_url.startswith('thunder'):
        category, title, hashes = parse_thunder_url(link_url)
    elif link_url.startswith('http://'):
        category, title, hashes = parse_http_url(link_url)
        params['website'] = ''
    else:
        magnet_params = link_url.split('|')
        print magnet_params,len(magnet_params), len(magnet_params[0])
        if len(magnet_params) == 2 and len(magnet_params[0]) >= 32:
            hashes['btih'] = magnet_params[0]
            title = magnet_params[1]
            category = 'magnet'
            link_url = 'magnet:?xt=urn:btih:%s' % (magnet_params[0])

    return category, title, size, hashes




def parse_thunder_url(thunder_url):
        category = 'thunder'
        title = ''
        hashes = {}
        return category, title, hashes


def parse_ed2k_url(ed2k_url):
    category = 'ed2k'
    params = ed2k_url.split('|')
    hashes = dict()
    size = None
    if len(params)>= 3:
        title = params[2]
    if len(params) >=5:
        if params[1] == 'file':
            size = params[3]
            hash_value = params[4]
            try:
                size = float(size)
                if size>1024*1024*1024:
                    size = size/(1024*1024*1024) 
                    print size
                    size = "%0.1f G" % (size)
                else:
                    size = size/(1024*1024)
                    print size
                    size = "%0.1f M" % size
            except Exception, e:
                size = None
            
            hashes['ed2k'] = hash_value

    else:
        title = ''
    
    return category,title,size,hashes

def parse_magnet_url(link_url):
    category = 'magnet'
    title = ''
    hashes = dict()
    if link_url.startswith('magnet:?'):
        uri_params = link_url[8:]
        uri_params = link_url[8:].split('&')
        params = dict()
        for param in uri_params:
            kv = param.split('=')
            if len(kv) == 2:
                k = kv[0]
                v = kv[1]
                params[k] = v
        for k in params.keys():
            v = params.get(k)
            if k == 'dn':
                title = v
            elif k == 'xt' or k.startswith('xt.'):
                v_params = v.split(':')
                if len(v_params) == 3:
                    hash_type = v_params[1]
                    hash_value = v_params[2]
                    hashes[hash_type] = hash_value

    return category, title, hashes

def parse_http_url(link_url):
    return 'http', link_url, {'md5': to_md5(link_url)}




