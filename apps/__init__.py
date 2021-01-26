#!-*- coding:utf-8 -*-
from flask_bootstrap import Bootstrap

from apps.articie.view import article_bp
from apps.articie.views import article_bp1
from apps.goods.view import goods_bp
from apps.user.views import user_bp1

__author__ = 'ALX LIN'
from flask import Flask
import setting
from exts import db, bootstrap
# from apps.user.view import user_bp
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(setting.DevelopmentConfig)
    #初始化配置db
    db.init_app(app=app)
    #初始化bootstrap
    bootstrap.init_app(app=app)
    #注册蓝图
    # app.register_blueprint(user_bp)
    app.register_blueprint(article_bp1)
    # app.register_blueprint(goods_bp)
    app.register_blueprint(user_bp1)
    print(app.url_map)
    return app