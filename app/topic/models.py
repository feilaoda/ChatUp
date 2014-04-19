"""
Topic:
    topic must be in a node

    impact:
        for sorting topic

        1. when user reply a topic, impact increase:
            + (n1 + day_del * n2) * log(user.reputation)

        2. when user up vote a topic, impact increase:
            + n3 * log(user.reputation)

        3. when user down vote a topic, impact decrease:
            - n4 * log(user.reputation)

"""

from datetime import datetime
import time

from dojang.database import db
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship, backref
from tornado.options import options


def get_current_impact():
    return int(time.time())


class Topic(db.Model):
    id = Column(Integer, primary_key=True)
    people_id =  Column(Integer, ForeignKey('people.id'), index=True)
    node_id =  Column(Integer, ForeignKey('topic_node.id'), index=True)
    title = Column(String(500))
    content = Column(Text)
    format = Column(String(100), default='html')
    status = Column(String(50)) #open, blocked, close
    hits = Column(Integer, default=1)
    impact = Column(Float, default=0)
    hidden = Column(String(1))
    up_count = Column(Integer, default=0)
    ups = Column(Text)  # e.g.  1,2,3,4
    down_count = Column(Integer, default=0)
    downs = Column(Text)  # e.g.  1,2,3,4
    reply_count = Column(Integer, default=0)
    last_reply_by = Column(Integer)
    last_reply_time = Column(DateTime, default=datetime.utcnow, index=True)
    
    created = Column(DateTime, default=datetime.utcnow)
    
    replies = relationship("TopicReply", backref="topic")

    def to_dict(self):
        r = dict()
        r["topic_id"] = self.id
        if self.people:
           r['people'] = self.people.to_dict()
        
        # if self.node:
        #     r['node'] = self.node.to_dict()
        r["title"] = self.title
        r["content"] = self.content
        r['status'] = self.status
        r['up_count'] = self.up_count
        r['down_count'] = self.down_count
        r['reply_count'] = self.reply_count
        if self.last_replyer:
           r['last_replyer'] = self.last_replyer.to_dict()
        r['last_reply_time'] = self.last_reply_time.strftime('%Y-%m-%d %H:%M:%S')
        r['created'] = self.created.strftime('%Y-%m-%d %H:%M:%S')

        return r

class TopicReply(db.Model):
    id = Column(Integer, primary_key=True)
    topic_id =  Column(Integer, ForeignKey('topic.id'), index=True)
    people_id =  Column(Integer, ForeignKey('people.id'), index=True)
    content = Column(String(2000))
    order =  Column(Integer, default=1, index=True)
    hidden = Column(String(1))
    up_count = Column(Integer, default=0)
    ups = Column(Text)  # e.g.  1,2,3,4
    created = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        r = dict()
        r["reply_id"] = self.id
        r["topic_id"] = self.topic_id
        if self.people:
            r['people'] = self.people.to_dict()
        r["content"] = self.content
        r["order"] = self.order
        r["hidden"] = self.hidden

        return r


class TopicVote(db.Model):
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, index=True)
    topic_id = Column(Integer, nullable=False, index=True)
    value = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)


class TopicLog(db.Model):
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, nullable=False, index=True)
    people_id = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
