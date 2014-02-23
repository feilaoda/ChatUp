from datetime import datetime
import hashlib
from random import choice

from dojang.database import db
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float
from tornado.options import options


class Search(db.Model):
    __tablename__ = "search"
    id = Column(Integer, primary_key=True)
