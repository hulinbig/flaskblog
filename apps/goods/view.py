#!-*- coding:utf-8 -*-
from flask import Blueprint, render_template, request

from apps.goods.models import Goods, User_goods
from apps.user.models import User
from exts import db

__author__ = 'ALX LIN'

goods_bp = Blueprint('goods', __name__)

@goods_bp.route('/findgoods')
def find_goods():
    user_id = request.args.get('uid')
    user = User.query.get(user_id)
    return render_template('goods/findfoods.html', user=user)



@goods_bp.route('/finduser')
def find_user():
    goods_id = request.args.get('gid')
    goods = Goods.query.get(goods_id)
    return render_template('goods/finduser.html', goods=goods)



@goods_bp.route('/show')
def show():
    users = User.query.filter(User.isdelete == False).all()
    good_list = Goods.query.all()
    return render_template('goods/show.html', users=users, good_list=good_list)



@goods_bp.route('/buy')
def buy():
    #uid,gid是前端传参地址的参数，以便正确插入数据
    uid = request.args.get('uid')
    gid = request.args.get('gid')
    ug = User_goods()
    ug.user_id = uid
    ug.goods_id = gid
    db.session.add(ug)
    db.session.commit()
    return '购买成功'


@goods_bp.route('/hah')
def hah():
    user_id = request.args.get('goodsid')
    goods = Goods.query.get(user_id)
    return render_template('goods/huhaha.html', goods=goods)