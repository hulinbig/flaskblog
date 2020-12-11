#!-*- coding:utf-8 -*-
__author__ = 'ALX LIN'
from flask import Blueprint,request, render_template,redirect,url_for
from apps.user.models import User
from exts import db
import hashlib
from sqlalchemy import or_,and_
user_bp1 = Blueprint('user', __name__, url_prefix='/user')

@user_bp1.route('/')
def index():
    return render_template('base.html')

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
            return '注册成功'
        else:
            return '二次密码不一致'
    return render_template('user/register.html')