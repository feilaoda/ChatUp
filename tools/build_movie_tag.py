# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import os
import sys
import urllib2
import re
import json

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
    print PROJDIR
    print('Development of keepcd')

from dojang.util import parse_config_file



def run_command():
    
    from keepcd.movie.models import Movie, MovieImage
    from dojang.database import SQLAlchemy, db
    from sqlalchemy import Column
    from sqlalchemy import Integer, String, DateTime, Text, Float
    from datetime import datetime
    from tornado.options import options
    import shutil
    from keepcd.movie.models import MovieTag
    from keepcd.tag.models import Tag,CAGETORY_TAG,COUNTRY_TAG,YEAR_TAG
    from keepcd.search.models import SearchMovie

    def query_tag(db, v, tag_type):
        if v is None:
            return None
        v = v.strip()
        tag = Tag.query.filter_by(value=v, type=tag_type).first()
        if tag is None:
            tag = Tag()
            tag.value = v
            tag.type = tag_type
            db.session.add(tag)
            db.session.commit()
        return tag    

    def build_movie_tag(db, movie_id, tag):
        if tag is None:
            return
        movie_tag = MovieTag.query.filter_by(movie_id=movie_id, tag_id=tag.id).first()
        if movie_tag is None:
            movie_tag = MovieTag()
            movie_tag.movie_id = movie_id
            movie_tag.tag_id = tag.id
            db.session.add(movie_tag)
            db.session.commit()


    # print options.sqlalchemy_db_from
    # db_from = SQLAlchemy(options.sqlalchemy_db_from)
    
    movies = Movie.query.filter_by().all()
    print len(movies)
    for movie in movies:
        print movie.id
        year = movie.year
        
        country = movie.country
        publish_time = movie.publish_time
        title = movie.title

        tag1 = query_tag(db, year, YEAR_TAG)
        build_movie_tag(db, movie.id, tag1)

        if country:
            countries = country.split('/')
            for c in countries:
                tag2 = query_tag(db, c, COUNTRY_TAG)
                build_movie_tag(db, movie.id, tag2)
        # tag2 = query_tag(db, country)
        # build_movie_tag(db, movie.id, tag2, COUNTRY_TAG)

        if movie.category:
            categorys = movie.category.split('/')
            for cat in categorys:
                tag3 = query_tag(db, cat, CAGETORY_TAG)
                build_movie_tag(db, movie.id, tag3)
        else:
            print "movie %d category is null" % (movie.id)
        search_movie = SearchMovie.query.filter_by(movie_id=movie.id).first()
        if search_movie is None:
            search_movie = SearchMovie()
            search_movie.movie_id = movie.id
            search_movie.published=0
        search_movie.title = movie.title
        search_movie.rating = movie.rating
        try:
            m = re.findall('\d{4}\-\d{1,2}\-\d{1,2}', movie.publish_time)

            if len(m) >= 1:
                search_movie.publish_time = m[0]
            elif year:
                search_movie.publish_time = '%s-01-01' % (year)
            else:
                search_movie.publish_time = '0000-01-01'
        except Exception, e:
            print movie.title, movie.publish_time
            raise

        
        db.session.add(search_movie)
        db.session.commit()
        # tag4 = query_tag(db, publish_time)
        # build_movie_tag(db, movie.id, tag4.id)
         




def main():
    parser = argparse.ArgumentParser(
        prog='keep cd',
        description='keep',
    )
    parser.add_argument('command', nargs="*")
    args = parser.parse_args()

    parse_config_file("../settings.py")

    run_command()




if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf8') 
    main()


