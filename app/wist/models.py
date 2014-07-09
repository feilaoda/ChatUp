from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float, UnicodeText
from sqlalchemy.orm import relationship, backref

from dojang.database import db



class Wist(db.Model):
    __tablename__="wist"
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, ForeignKey('people.id'), index=True)
    username = Column(String(100))
    #token = Column(String(16), default=0, index=True)
    fork_root_id = Column(Integer, default=0, index=True)
    fork_from_id = Column(Integer, default=0, index=True)
    fork_from_username = Column(String(100))
    star_count = Column(Integer, default=0)
    fork_count = Column(Integer, default=0)
    tags = Column(String(255))
    title = Column(String(500))
    content_id =  Column(Integer, ForeignKey('wist_content.id'))
    created = Column(DateTime, default=datetime.utcnow)
    # wist = relationship("Wist", backref="content")
    star = relationship("WistStar", backref="wist")


class WistContent(db.Model):
    __tablename__="wist_content"
    id = Column(Integer, primary_key=True)
    content = Column(UnicodeText)
    content_html = Column(UnicodeText)
    created = Column(DateTime, default=datetime.utcnow)
    wist = relationship("Wist", backref="content")

class WistForkGraph(db.Model):
    __tablename__="wist_fork_graph"
    id = Column(Integer, primary_key=True)
    fork_root_id = Column(Integer, default=None, index=True)
    fork_count = Column(Integer, default=0)
    

class WistStar(db.Model):
    __tablename__="wist_star"
    id = Column(Integer, primary_key=True)
    wist_id = Column(Integer, ForeignKey('wist.id'), index=True)
    people_id = Column(Integer, default=None, index=True)
    created = Column(DateTime, default=datetime.utcnow)

    

