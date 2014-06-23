from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship, backref

from dojang.database import db



class Wist(db.Model):
    __tablename__="wist"
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, ForeignKey('people.id'), index=True)
    fork_root_id = Column(Integer, default=None, index=True)
    fork_from_id = Column(Integer, default=None, index=True)
    fork_url = Column(String(500))
    title = Column(String(500))
    content_id =  Column(Integer, ForeignKey('wist_content.id'))
    # content =  Column(Text)
    # content_html = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)


class WistContent(db.Model):
    __tablename__="wist_content"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    content_html = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)
    wist = relationship("Wist", backref="content")
