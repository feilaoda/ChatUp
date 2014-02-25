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


class PushGroup(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    create_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        r = dict()
        r['id'] = self.id
        r['title'] = self.title
        
        return r



class PushChannel(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    people_id = Column(Integer, nullable=False, index=True)
    group_id = Column(Integer, nullable=False, index=True)
    #0: public
    #1: private
    permission = Column(Integer, default=0, index=True)
    token = Column(String(64))
    summary = Column(Text)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        r = dict()
        r['id'] = self.id
        r['name'] = self.name
        r['title'] = self.title
        r['summary'] = self.summary
        r['update_at'] = self.update_at.strftime('%Y-%m-%d %H:%M:%S')
        # if self.format is not None:
        #     r['format'] = self.format
        return r

        
class PushChannelText(db.Model):
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, nullable=False, default=0, index=True)
    title = Column(String(200))
    format = Column(String(32))
    content = Column(Text)
    create_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        r = dict()
        r['id'] = self.id
        r['format'] = self.format
        r['content'] = self.content
        r['create_at'] = self.create_at.strftime('%Y-%m-%d %H:%M:%S')

class PushText(db.Model):
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, default=0, index=True)
    content = Column(Text)
    sync = Column(Integer, default=0, index=True)
    create_at = Column(DateTime, default=datetime.utcnow)



