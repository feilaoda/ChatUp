import hashlib
from random import choice
from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float
from tornado.options import options
from dojang.database import db



class Search(db.Model):
    __tablename__ = "search"
    id = Column(Integer, primary_key=True)
