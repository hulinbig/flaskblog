#!-*- coding:utf-8 -*-
__author__ = 'ALX LIN'
from exts import db
from datetime import datetime

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pdatatime=db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    #外键 同步到数据库的外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
