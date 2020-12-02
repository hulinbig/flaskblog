#!-*- coding:utf-8 -*-
from flask import Blueprint, request, render_template

from apps.articie.models import Article
from apps.user.models import User
from exts import db

__author__ = 'ALX LIN'

article_bp = Blueprint('article', __name__)

@article_bp.route('/publish', methods = ['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        uid = request.form.get('uid')
        #添加文章
        article = Article()
        article.title = title
        article.content = content
        article.user_id = uid
        db.session.add(article)
        db.session.commit()
        return '添加成功'
    else:
        users = User.query.filter(User.isdelete == False).all()
        return render_template('article/add_article.html', users=users)

#根据文章找作者
@article_bp.route('/all')
def article_all():
    articles = Article.query.all()
    return render_template('article/all.html', articles=articles)

#根据作者找文章
@article_bp.route('/all1')
def article_all1():
    id = request.args.get('id')
    user = User.query.get(id)
    return render_template('article/all1.html', user=user)