#!-*- coding:utf-8 -*-
__author__ = 'ALX LIN'
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session
from apps.user.models import User
from exts import db
import hashlib
from sqlalchemy import or_,and_
user_bp1 = Blueprint('user', __name__, url_prefix='/user')

@user_bp1.route('/')
def index():
    #1.cookie获取方式
    # uid = request.cookies.get('uid', None)
    #2.session的获取,session底层默认获取
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user)
    else:
        return render_template('user/index.html')

@user_bp1.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if password == repassword:
            user = User()
            user.username = username
            user.password = hashlib.md5(password.encode('utf-8')).hexdigest()
            user.phone = phone
            user.email = email
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.index'))
        else:
            return '二次密码不一致,请重新输入'
    return render_template('user/register.html')

@user_bp1.route('/checkphone', methods=['POST', 'GET'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    print(user)
    #code 400 不能用 200可以用
    if len(user) > 0:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可用')


@user_bp1.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = hashlib.md5(request.form.get('password').encode('utf-8')).hexdigest()
        user_list = User.query.filter_by(username=username)
        us = User.query.filter(User.username ==username)
        for user in user_list:
            if user.password == password:
                #1.cookie实现机制
                # response = redirect(url_for('user.index'))
                # response.set_cookie('uid', str(u.id), max_age=3600)
                # return response
                #2.session实现机制
                session['uid'] = user.id
                return redirect(url_for('user.index'))
            else:
                return render_template('user/login.html', msg='用户名或密码错误')
    return render_template('user/login.html')


@user_bp1.route('/logout')
def logout():
    #1.cookie的方式
    # response = redirect(url_for('user.index'))
    # #通过response对象的delete_cookie(key),key就是要删除的cookie的key
    # response.delete_cookie('uid')
    #2.session的方式
    # del session['uid'] #用户退出后，开辟的session的空间不会被清除
    session.clear()#用户退出后，将开辟的session的空间一起删除，净删除
    return redirect(url_for('user.index'))

@user_bp1.route('/sendMsg')
def send_message():
    pass