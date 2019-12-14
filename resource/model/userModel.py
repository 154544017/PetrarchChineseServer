# -*- coding: utf-8 -*-

from resource import db


class User(db.Model):
    """用户角色/身份表"""
    __tablename__ = "rs_user"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<User {}>'.format(self.name)
