
import hashlib
from random import choice
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Text, Float
from tornado.options import options
from dojang.database import db

CAGETORY_TAG=1
COUNTRY_TAG=2
YEAR_TAG=3

class Tag(db.Model):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    value = Column(String(250), nullable=False, index=True)
    type = Column(String(30), nullable=False, index=True)
    created = Column(DateTime, default=datetime.utcnow)





