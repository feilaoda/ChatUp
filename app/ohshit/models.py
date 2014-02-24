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


class Ohmy(db.Model):
    __tablename__="oh_my"
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, index=True)
    start = Column(DateTime, default=datetime.utcnow)
    end = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer, default=0)
    day = Column(String(10), index=True)
    create_at = Column(DateTime, default=datetime.utcnow)


class OhStat(db.Model):
    __tablename__="oh_stat"
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, index=True)
    level = Column(Float, default=0)
    day = Column(String(10), index=True)
    create_at = Column(DateTime, default=datetime.utcnow)

class OhStatHistory(db.Model):
    __tablename__="oh_stat_history"
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, index=True)
    level = Column(Float, default=0)
    day = Column(String(10), index=True)
    create_at = Column(DateTime, default=datetime.utcnow)
