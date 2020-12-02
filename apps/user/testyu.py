#!-*- coding:utf-8 -*-
__author__ = 'ALX LIN'
import hashlib

msg = 'this is a word'
md5 = hashlib.md5(msg.encode('utf-8'))
print(md5)
r = md5.hexdigest()
print(r)