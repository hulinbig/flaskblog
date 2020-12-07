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

