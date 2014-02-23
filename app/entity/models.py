"""
Entity

"""

from datetime import datetime
import hashlib
from random import choice

from dojang.database import db
from dojang.util import create_token
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, backref
from tornado.options import options


class Entity(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    aliases = Column(String(200), nullable=True)
    description = Column(Text)
    isa = Column(String(200), nullable=False)
    statements = Column(Text)
    salt = Column(String(32), index=True)
    created = Column(DateTime, default=datetime.utcnow)

    people_added_links = relationship("PeopleAddedLink", backref="entity")

    def __init__(self):
        salt = create_token(32)