#!-*- coding:utf-8 -*-
__author__ = 'ALX LIN'
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from apps.user.models import User
from exts import db
import hashlib
from sqlalchemy import or_,and_
user_bp1 = Blueprint('user', __name__, url_prefix='/user')

@user_bp1.route('/')
def index():
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
            return '二次密码不一致'
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
        for u in user_list:
            if u.password == password:
                return redirect(url_for('user.index'))



            else:
                return render_template('user/login.html', msg='用户名或密码错误')
    return render_template('user/login.html')

@user_bp1.route('/test')
def test():
    return render_template('user/hah.html')