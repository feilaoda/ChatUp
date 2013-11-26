# -*- coding: utf-8 -*-
"""
People:
    only the basic info of a user

    role:
        staff > 6
        admin > 9
        active > 1
        not verified email = 1
        deactive < 1

    reputation:
        reputation means the value of a member, it affects in topic and
        everything

        1. when user's topic is up voted, reputation increase:
            + n1 * log(user.reputation)

        2. when user's topic is down voted, reputation decrease:
            - n2 * log(user.reputation)

"""
import urllib
import hashlib
from random import choice
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Text
from tornado.options import options
from dojang.database import db
from dojang.util import to_md5


class People(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    nickname = Column(String(100), unique=True, index=True)
    email = Column(String(200), nullable=True)
    password = Column(String(100), nullable=True)
    avatar = Column(String(400))
    website = Column(String(400))

    role = Column(Integer, default=2)
    # 0: registered,  1: username
    reputation = Column(Integer, default=100, index=True)
    token = Column(String(16))

    city = Column(String(200))
    status = Column(Integer, default=0)
    description = Column(Text)
    follow_count = Column(Integer, default=0)
    followed_count = Column(Integer, default=0)

    # setting = relationship("PeopleSetting", backref="people")
    # duedate = Column(DateTime)
    created = Column(DateTime, default=datetime.utcnow)

    def __init__(self, username, **kwargs):
        #self.email = email.lower()
        self.username = username
        self.token = self.create_token(16)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_avatar(self, size=48):
        if self.avatar is None:
            default = options.static_avatar_default
            #if self.email is None:
            return options.static_avatar_default

            # md5email = hashlib.md5(self.email.lower()).hexdigest()
            # # query = "%s?s=%s%s&d=%s" % (md5email, size, options.gravatar_extra, options.static_avatar_default)
            # gravatar_url = "http://www.gravatar.com/avatar/" + md5email + "?"
            # gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            # return gravatar_url
        return self.avatar
        #md5email = hashlib.md5(self.email).hexdigest()
        #query = "%s?s=%s%s" % (md5email, size, options.gravatar_extra)
        #return options.gravatar_base_url + query

    def get_notification(self):
        count = Notification.query.filter_by(readed='n')\
                .filter_by(receiver=self.id).count()
        return count

    def to_json(self):
        data = (
            '{"username":"%s", "avatar":"%s", "website":"%s",'
            '"reputation":%s, "role":%s}'
        ) % (self.username, self.get_avatar(), self.website or "",
             self.reputation, self.role)
        return data

    def to_dict(self):
        r = dict()
        r['people_id'] = self.id
        r['username'] = self.username
        r['avatar'] = self.avatar
        r['nickname'] = self.nickname
        r['email'] = self.email
        r['follow_count'] = self.follow_count
        r['followed_count'] = self.followed_count
        
        return r

    @staticmethod
    def create_password(raw):
        md5_raw = to_md5(to_md5(raw))
        salt = People.create_token(8)
        hsh = hashlib.sha1(salt + md5_raw + options.password_secret).hexdigest()
        return "%s$%s" % (salt, hsh)

    @staticmethod
    def create_token(length=16):
        chars = ('0123456789'
                 'abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        salt = ''.join([choice(chars) for i in range(length)])
        return salt

    def check_password(self, raw):
        if '$' not in self.password:
            return False
        salt, hsh = self.password.split('$')
        verify = hashlib.sha1(salt + raw + options.password_secret).hexdigest()
        return verify == hsh

    @property
    def is_staff(self):
        return self.role >= 6

    @property
    def is_admin(self):
        return self.role >= 9
    
class PeopleSetting(db.Model):
    __tablename__="people_setting"
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=False, index=True)
    #状态类型: 0:其他  1:备孕  2:怀孕中  3:宝贝已出生
    stat_type = Column(Integer, default=0)
    stat_date = Column(DateTime) #预产期或宝贝出生日期
    pregnancy_babycount = Column(Integer, default=1)
    pregnancy_week = Column(Integer, default=0)
    pregnancy_day = Column(Integer, default=0)



# class PeopleFollower(db.Model):
#     __tablename__="people_follower"
#     id = Column(Integer, primary_key=True)
#     people_id = Column(Integer, nullable=False, index=True)
#     target_id = Column(Integer, nullable=False, index=True)
#     created = Column(DateTime, default=datetime.utcnow)

class Notify(db.Model):
    id = Column(Integer, primary_key=True)
    sender = Column(Integer, nullable=False)
    receiver = Column(Integer, nullable=False, index=True)

    content = Column(String(400))
    refer = Column(String(600))

    type = Column(String(20), default='mention')
    created = Column(DateTime, default=datetime.utcnow)
    readed = Column(String(1), default='n')


class Social(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    enabled = Column(String(1), default='y')
    service = Column(String(100))  # service name: twitter, douban
    token = Column(Text)


class Weibo(db.Model):
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, nullable=True, index=True)
    uid = Column(String(30), nullable=False, index=True)
    domain = Column(String(100))
    name = Column(String(100))
    screen_name = Column(String(100))
    province = Column(String(100))
    city = Column(String(100))
    location = Column(String(100))
    avatar_small = Column(String(200))
    avatar_large = Column(String(200))
    token = Column(Text)
    session_expires = Column(Integer)

