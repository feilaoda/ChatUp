"""
Space Topic:
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

import time
from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship, backref
from dojang.database import db
from tornado.options import options

def get_current_impact():
    return int(time.time())


class Node(db.Model):
    __tablename__="space_node"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200), nullable=True, index=True)
    anonymous = Column(Integer, default=0, index=True) #0: all 1:app
    avatar = Column(String(400))
    description = Column(String(1000))
    created = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)
    sorting = Column(String(50), nullable=True, default="-id")
    topic_count = Column(Integer, default=0)

    topics = relationship("Topic", backref="node")

    def to_dict(self):
        r = dict()
        r['node_id'] = self.id
        r['name'] = self.name
        r['title'] = self.title
        r['category'] = self.category
        r['avatar'] = self.avatar
        r['last_updated'] = self.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        r['topic_count'] = self.topic_count
        return r



class FollowNode(db.Model):
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, index=True)
    node_id = Column(Integer, nullable=False, index=True)
    created = Column(DateTime, default=datetime.utcnow)


class Topic(db.Model):
    __tablename__="space_topic"
    id = Column(Integer, primary_key=True)
    people_id =  Column(Integer, ForeignKey('people.id'), index=True)
    node_id =  Column(Integer, ForeignKey('space_node.id'), index=True)
    nickname = Column(String(100), default='Anonymous')
    title = Column(String(500))
    content = Column(Text)    
    format = Column(String(100), default='html')
    status = Column(String(50)) #open, blocked, close
    hits = Column(Integer, default=1)
    anonymous = Column(Integer, default=1)
    up_count = Column(Integer, default=0)
    ups = Column(Text)  # e.g.  1,2,3,4
    down_count = Column(Integer, default=0)
    downs = Column(Text)  # e.g.  1,2,3,4
    reply_count = Column(Integer, default=0)
    last_reply_time = Column(DateTime, default=datetime.utcnow, index=True)
    created = Column(DateTime, default=datetime.utcnow)
    replies = relationship("TopicReply", backref="topic")

    def to_dict(self):
        r = dict()
        r["topic_id"] = self.id
        r["username"] = self.username
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
        r['last_reply_time'] = self.last_reply_time.strftime('%Y-%m-%d %H:%M:%S')
        r['created'] = self.created.strftime('%Y-%m-%d %H:%M:%S')

        return r

class TopicReply(db.Model):
    __tablename__="space_reply"
    id = Column(Integer, primary_key=True)
    topic_id =  Column(Integer, ForeignKey('space_topic.id'), index=True)
    people_id =  Column(Integer, ForeignKey('people.id'), index=True)
    nickname = Column(String(100), default='Anonymous')
    content = Column(String(2000))
    order =  Column(Integer, default=1, index=True)
    anonymous = Column(Integer, default=1)
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
