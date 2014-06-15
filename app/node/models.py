# -*- coding: utf-8 -*-

from datetime import datetime

from dojang.database import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, backref


class Node(db.Model):
    __tablename__="topic_node"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200), nullable=True, index=True)
    anonymous = Column(Integer, default='0', index=True) #0: all 1:app
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
        r['id'] = self.id
        r['name'] = self.name
        r['title'] = self.title
        r['category'] = self.category
        r['avatar'] = self.avatar
        r['last_updated'] = self.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        r['topic_count'] = self.topic_count
        return r





# class FollowNode(db.Model):
#     id = Column(Integer, primary_key=True)
#     people_id = Column(Integer, nullable=False, index=True)
#     node_id = Column(Integer, nullable=False, index=True)
#     created = Column(DateTime, default=datetime.utcnow)
