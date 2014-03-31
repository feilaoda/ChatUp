"""


"""

from datetime import datetime
import hashlib
from random import choice

from dojang.database import db
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship, backref
from tornado.options import options


class Group(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    people_id = Column(Integer, nullable=False, index=True)
    tag = Column(String(200))
    #0: any people can join
    #1: invited friends can join
    permission = Column(Integer, default=0, index=True)
    #0: forever  1:1hour  24:24hours
    timeup = Column(Integer, default=0, index=True)
    #1:open  0:frozen
    status = Column(Integer, default=1, index=True)
    avatar = Column(String(400), nullable=True)
    # color = Column(String(30))

    people_count = Column(Integer, default=0)

    created = Column(DateTime, default=datetime.utcnow)

    def followed_by(self, people):
        return false

class GroupFollow(db.Model):
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, index=True)
    group_id = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, default=datetime.utcnow)



class GroupThread(db.Model):
    id = Column(Integer, primary_key=True)
    people_id =  Column(Integer, ForeignKey('people.id'), index=True)
    group_id =  Column(Integer, ForeignKey('group.id'), index=True)
    title = Column(String(500))
    content = Column(Text)
    format = Column(String(100), default='bbcode')
    status = Column(String(50)) #open, blocked, close
    hits = Column(Integer, default=1)
    impact = Column(Float, default=0)
    delete = Column(String(1))
    up_count = Column(Integer, default=0)
    ups = Column(Text)  # e.g.  1,2,3,4
    down_count = Column(Integer, default=0)
    downs = Column(Text)  # e.g.  1,2,3,4
    reply_count = Column(Integer, default=0)
    last_reply_by = Column(Integer)
    last_reply_time = Column(DateTime, default=datetime.utcnow, index=True)
    created = Column(DateTime, default=datetime.utcnow)
    replies = relationship("GroupThreadReply", backref="thread")


class GroupThreadReply(db.Model):
    id = Column(Integer, primary_key=True)
    thread_id =  Column(Integer, ForeignKey('group_thread.id'), index=True)
    people_id =  Column(Integer, ForeignKey('people.id'), index=True)
    content = Column(String(2000))
    orders =  Column(Integer, default=1, index=True)
    created = Column(DateTime, default=datetime.utcnow)
