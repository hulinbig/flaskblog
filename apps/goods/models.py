#!-*- coding:utf-8 -*-
from exts import db

__author__ = 'ALX LIN'

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.String(200))

    def __str__(self):
        return self.gname

#关系中间表，用户与商品之间的关系
class User_goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    number = db.Column(db.Integer, default=1)