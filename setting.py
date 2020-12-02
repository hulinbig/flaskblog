#!-*- coding:utf-8 -*-
__author__ = 'ALX LIN'
class Config:
    ENV = 'development'
    DEBUG = True
    #mysql + pymysql://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/blog"   #这里只能用localhost，不能用本家地址127.0.0.1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class DevelopmentConfig(Config):
    ENV = 'development'

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False