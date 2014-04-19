# -*- coding: utf-8 -*-

from datetime import datetime
import time

from dojang.database import db
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship, backref
from tornado.options import options


class ThreadNode(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    thread_count = Column(Integer, default=0)
    order_index = Column(Integer, default=0)

    def to_dict(self):
        r = dict()
        r["id"] = self.id
        r["title"]  = self.title
        r["thread_count"] = self.thread_count
        r["order_index"] = self.order_index
        return r

class Thread(db.Model):
    id = Column(Integer, primary_key=True)
    people_id =  Column(Integer, ForeignKey('people.id'), index=True)
    node_id =  Column(Integer, ForeignKey('thread_node.id'), index=True)
    content = Column(Text)
    status = Column(String(50)) #open, blocked, close
    hits = Column(Integer, default=1)
    hidden = Column(String(1))
    up_count = Column(Integer, default=0)
    ups = Column(Text)  # e.g.  1,2,3,4
    down_count = Column(Integer, default=0)
    downs = Column(Text)  # e.g.  1,2,3,4
    created = Column(DateTime, default=datetime.utcnow)


    def to_dict(self):
        r = dict()
        r["id"] = self.id
        if self.people:
           r['people'] = self.people.to_dict()
        r["content"] = self.content
        r['status'] = self.status
        r['hidden'] = self.hidden
        r['up_count'] = self.up_count
        r['down_count'] = self.down_count
        r['created'] = self.created.strftime('%Y-%m-%d %H:%M:%S')
        return r
