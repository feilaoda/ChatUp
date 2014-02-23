from datetime import datetime

from dojang.database import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, backref


class Shot(db.Model):
    __tablename__="shot"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=True)
    tag = Column(String(200), nullable=True)
    small_url = Column(String(500))
    large_url = Column(String(500))
    use_cdn = Column(String(50), default="cdn1")
    cdn1 = Column(String(500))
    cdn2 = Column(String(500))
    cdn3 = Column(String(500))
    up_count = Column(Integer, default=0)

