"""


"""

import hashlib
from random import choice
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Text
from tornado.options import options
from dojang.database import db



class Group(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    people_id = Column(Integer, nullable=False, index=True)
    tag = Column(String(200))
    #0: any people can join
    #1: invited friends can join
    permission = Column(Integer, default=0, index=True)
    #1:open  0:close
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
