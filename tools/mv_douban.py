# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import json
import os
import re
import sys
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

    print PROJDIR, ROOTDIR
    import keepcd
    print('Development of keepcd')



def mkdir_p(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

def has_chinese(s):
    for c in s:
        if c >= u'\u4e00' and c<=u'\u9fa5':
            return True
    return False

def run_command():
    
    from keepcd.movie.models import Movie, MovieImage,MovieSite
    from keepcd.entity.models import Entity
    from dojang.database import SQLAlchemy, db
    from sqlalchemy import Column
    from sqlalchemy import Integer, String, DateTime, Text, Float
    from datetime import datetime
    from tornado.options import options
    import shutil
    from watermark import watermark, MARKIMAGE, POSITION
    from keepcd.util import make_thumb, make_resize, download_douban_image

    print options.sqlalchemy_db_from
    db_from = SQLAlchemy(options.sqlalchemy_db_from)
    

    class DoubanMovie(db_from.Model):
        id = Column(Integer, primary_key=True)
        url = Column(String(200), nullable=True, index=True)
        title = Column(Text)
        description = Column(Text)
        thumb = Column(String(1000), nullable=True)
        thumb_file = Column(String(500), nullable=True)
        rating = Column(Float, nullable=True, default=0.0)
        year = Column(String(20), nullable=True)
        category = Column(String(200), nullable=True)
        country = Column(String(200), nullable=True)
        language = Column(String(200), nullable=True)
        directors = Column(String(200), nullable=True)
        actors = Column(String(250), nullable=True)
        writers = Column(String(200), nullable=True)
        alias_title = Column(String(1000), nullable=True)
        company = Column(String(200), nullable=True)
        official_site = Column(String(200), nullable=True)
        duration = Column(String(200), nullable=True)
        publish_time = Column(String(50), nullable=True)
        imdb_id = Column(Integer)
        created = Column(DateTime, default=datetime.utcnow)
        updated = Column(DateTime, default=datetime.utcnow)
        is_parsed = Column(Integer)

    


    douban_movies = DoubanMovie.query.filter_by().limit(500).all()

    for movie in douban_movies:
        imdb_id = movie.imdb_id
        new_movie = Movie.query.filter_by(imdb_id=imdb_id).first()
        movie_image = None
        entity = None
        if new_movie:
            entity = Entity.query.filter_by(id=new_movie.id).first()
            movie_image = MovieImage.query.filter_by(id=new_movie.image_id).first()
        if not entity:
            entity = Entity()
            entity.isa = "movie"
            entity.label = movie.title

        db.session.add(entity)
        db.session.commit()
        if not new_movie:        
            new_movie = Movie()
            new_movie.id = entity.id
        
        if new_movie.id != entity.id:
            new_movie.id = entity.id

        is_chinese = has_chinese(movie.title)
        if is_chinese:
            blank_pos = movie.title.find(" ")
            if blank_pos > 0:
                new_movie.title = movie.title[:blank_pos]
                new_movie.extra_title = movie.title[blank_pos+1:]
            else:
                new_movie.title = movie.title
                new_movie.extra_title = None
                
        else:
            new_movie.title = movie.title
            new_movie.extra_title = None
        
        # print movie.title,"->", new_movie.title, "->", new_movie.extra_title

        m = re.findall("\d+", movie.url)

        if len(m) >= 1:
            new_movie.douban_id = int(m[0])


        new_movie.description = movie.description
        if movie.rating:
            new_movie.rating = float(movie.rating)
        else:
            new_movie.rating = 0
        new_movie.year = movie.year
        new_movie.category = movie.category
        new_movie.country = movie.country
        new_movie.language = movie.language
        new_movie.directors = movie.directors
        new_movie.actors = movie.actors
        new_movie.writers = movie.writers
        new_movie.alias_title = movie.alias_title
        new_movie.company = movie.company
        new_movie.official_site = movie.official_site
        new_movie.duration = movie.duration
        if movie.publish_time:
            new_movie.publish_time = movie.publish_time
        else:
            new_movie.publish_time = movie.year
        new_movie.imdb_id = movie.imdb_id

        if movie_image is None:
            movie_image = MovieImage()

        if movie.thumb_file:
            to_prefix = "/Users/zhenng/Work/python/keepcd/keepcd/static/movies/"
            res,movie_image.thumb, movie_image.small,  movie_image.large = download_douban_image(new_movie.douban_id, 
                    movie.thumb, to_prefix)
            db.session.add(movie_image)
            db.session.commit()
            new_movie.image_id = movie_image.id

        # prefix = "e:/source/python/easy_crawl/"
        # from_path = prefix + movie.thumb_file
        # to_prefix = "e:/source/python/keepcd/keepcd/static/movies/"
        
        # douban_id = str(new_movie.douban_id)

        # paths = movie.thumb_file.split('/')
        # image_filename = paths[-1]
        
        # large_split_name = "large/" + "/".join(paths[2:-1]) + "/l" + image_filename[1:]
        
        # small_split_name = "small/" + "/".join(paths[2:-1]) + "/s" + image_filename[1:]
        # thumb_split_name = "small/" + "/".join(paths[2:-1]) + "/t" + image_filename[1:]

        # small_path = to_prefix + small_split_name
        # thumb_path = to_prefix + thumb_split_name
        # large_path = to_prefix + large_split_name

        # # print large_path
        # # print thumb_path
        
        # mkdir_p(os.path.dirname(thumb_path))
        # make_thumb(from_path, thumb_path , 75)

        # make_resize(from_path, small_path, 150, 200)

        # mkdir_p(os.path.dirname(large_path))
        # shutil.copyfile(from_path, large_path)

        # watermark(large_path,"miniwater.png",'RIGHTTOP',opacity=0.8).save(large_path,quality=100)
        # watermark(large_path,"water.png",'CENTERBOTTOM',opacity=0.5).save(large_path,quality=100)

        # watermark(small_path,"miniwater.png",'CENTERTOP',opacity=0.2).save(small_path,quality=100)

        # img_domain_prefix = "" #"http://www.keepcd.com"
        # movie_image.small = img_domain_prefix + "/static/movies/"+ small_split_name;
        # movie_image.thumb = img_domain_prefix + "/static/movies/"+ thumb_split_name;
        # movie_image.large = img_domain_prefix + "/static/movies/"+ large_split_name;



        
        db.session.add(new_movie)
        db.session.commit()

        movie_link = MovieSite.query.filter_by(movie_id=new_movie.id, website=0).first()
        if movie_link is None:
            movie_link = MovieSite()
            movie_link.movie_id = new_movie.id
            movie_link.website = "douban"
        if movie.rating:
            movie_link.rating = float(movie.rating)
        else:
            movie_link.rating = 0
        movie_link.site_url = movie.url
        db.session.add(movie_link)
        db.session.commit()


        # print movie.thumb

    # movies = Movie.query.filter_by().all()
    # for movie in movies:
    #     print movie.title

 

def main():
    parser = argparse.ArgumentParser(
        prog='keep cd',
        description='keep',
    )
    parser.add_argument('command', nargs="*")
    args = parser.parse_args()

    parse_config_file("settings.conf")

    run_command()
    # if isinstance(args.command, basestring):
    #     run_command(args.command)
    # elif isinstance(args.command, (list, tuple)):
    #     for cmd in args.command:
    #         run_command(cmd)
    # else:
    #     run_command(args.command)


if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf8') 
    main()


