"""
Page

"""

import hashlib
from random import choice
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Text
from tornado.options import options
from dojang.database import db



class Channel(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), index=True)
    isa = Column(String(50))
    pic = Column(String(255))
    sorting = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)

    @property
    def entries(self):
        return ChannelEntry.query.filter_by(channel_id=self.id).order_by('sorting').all()

class ChannelEntry(db.Model):
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, index=True)
    entry_id = Column(Integer, index=True)
    title = Column(String(200), index=True)
    sorting = Column(Integer, index=True)
    url = Column(String(255))
    content = Column(Text)
    pic = Column(String(255))
    created = Column(DateTime, default=datetime.utcnow)

