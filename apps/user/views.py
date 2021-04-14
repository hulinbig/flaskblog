#!-*- coding:utf-8 -*-
import os

from werkzeug.utils import secure_filename

from apps.article.models import Article_type, Article
from setting import Config

__author__ = 'ALX LIN'
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session, g
from apps.user.models import User, Photo
from exts import db
import hashlib
from sqlalchemy import or_,and_
user_bp1 = Blueprint('user', __name__, url_prefix='/user')

#验证用户的登陆权限
required_login_list = ['/user/center', '/user/update', '/user/publish',
                       '/article/publish', '/article/detail', '/article/article_find',
                       '/user/upload_photo', '/user/del_photo', '/user/del_photo',
                       '/article/add_comment']
#flask钩子函数
@user_bp1.before_app_first_request
def first_request():
    print('before_app+first_request')

#重点****************
@user_bp1.before_app_request
def before_request1():
    print('before_request1before_request1', request.path)
    if request.path in required_login_list:
        id =session.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)
            #g对象，本次请求的对象
            g.user = user

@user_bp1.after_app_request
def after_request_test(response):
    response.set_cookie('a', 'bbb', max_age=19)
    print('after_request_test')
    return response

@user_bp1.teardown_app_request
def teardown_request(response):
    print('teardown_request_test')

#自定义过滤器
@user_bp1.app_template_filter('cdecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content[:50]#显示多少字符

@user_bp1.route('/')
def index():
    #1.cookie获取方式
    # uid = request.cookies.get('uid', None)
    #2.session的获取,session底层默认获取
    uid = session.get('uid')
    #接收页码数
    page = request.args.get('page', 1)
    if page == 'None':
        page = 1
    else:
        page = int(page)
    #获取文章列表,按照创建时间进行倒序排列
    pagination = Article.query.order_by(Article.pdatatime.desc()).paginate(page=page, per_page=5)
    print(pagination.items) #[<Article 9>, <Article 8>, <Article 4>] 拿到当前页的数据
    print(pagination.page)  #当前的页码数
    print(pagination.prev_num) #当前页的前一页页码数`
    print(pagination.next_num) #当前页的后一页页码数
    print(pagination.has_next) #bool 类型  判断是否有后一页
    print(pagination.has_prev)#bool 类型  判断是否有前一页
    print(pagination.pages) #总共有几页
    print(pagination.total) #总的记录条数
    #获取分类列表
    types = Article_type.query.all()
    #判断用户是否登陆
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, types=types, pagination=pagination)
    else:
        return render_template('user/index.html', types=types, pagination=pagination)

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
        f = int(request.args.get('f'))#用户名或密码
        if f == 1:
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
        elif f =='2':#手机号码于验证码
            phone = request.form.get('phone')
            code = request.form.get('code')
            #先去验证验证码
            valid_code = session.get(phone)
            if code == valid_code:
                #查询数据库
                user = User.query.filter(User.phone == phone).first()
                if user:
                    #登陆成功
                    session['uid'] = user.id
                    return redirect(url_for('user.index.html'))
                else:
                    return render_template('user/login.html', msg='此号码未注册')
            else:
                return render_template('user/login.html', msg='验证码有误！')
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

#用户中心
@user_bp1.route('/center')
def user_center():
    # id = session.get('uid')
    # user = User.query.get(id)
    types = Article_type.query.all()
    photos = Photo.query.order_by(Photo.photo_datetime.desc()).filter_by(user_id=g.user.id).all()
    return render_template('user/center.html', user=g.user, types=types, photos=photos)

ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif']
#修改用户信息
@user_bp1.route('/update',methods=['POST', 'GET'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        print('dd', phone, type(phone))
        email = request.form.get('email')
        #只要有图片，获取方式必须使用request.files.get(name)
        icon = request.files.get('icon')
        # print(icon)
        #查询手机号码
        # users = User.query.all()
        # for user in users:
        #     if user.phone == phone:
        #         #说明数据中已经有人注册此号码
        #         return render_template('user/center.html', user=g.user, msg='此号码已被注册不能使用')
        #属性：filename 用户获取文件的名字
        #方法：save(保存路径)
        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name) #保证文件名是符合python的命名规则,python的命名规则
            file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
            icon.save(file_path)
            #保存成功
            g.user.username = username
            g.user.phone = phone
            g.user.email = email
            path = 'upload/icon/'  #最后要加/，否则拼接出来的是反斜杠
            g.user.icon = os.path.join(path, icon_name)
            print('----------------------------------------------------------', g.user.icon)
            db.session.commit()
            # session.clear()  # 用户修改后，可退出登陆
            return redirect(url_for('user.user_center'))
        else:
            return render_template('user/center.html', user=g.user, msg='上传文件格式错误：请上传后缀为jpg, png, gif的文件')
    else:
        return render_template('user/center.html', user=g.user)


#上传照片
@user_bp1.route('/upload_photo', methods=['POST', 'GET'])
def upload_photo():
    if request.method == 'POST':
        photo = request.files.get('photo')
        print('--------------',photo)
        photo_name = photo.filename
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', photo_name)
        suffix = photo_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            photo_name = secure_filename(photo_name)  # 保证文件名是符合python的命名规则,python的命名规则
            file_path = os.path.join(Config.UPLOAD_PHOTO_DIR, photo_name)
            photo.save(file_path)
            # 保存成功
            path = 'upload/photo/'  # 最后要加/，否则拼接出来的是反斜杠
            sphone = Photo()
            sphone.photo_name = os.path.join(path, photo_name)
            sphone.user_id = g.user.id
            db.session.add(sphone)
            db.session.commit()
            return redirect(url_for('user.user_center'))
        else:
            return render_template('user/center.html', user=g.user, msg='上传文件格式错误：请上传后缀为jpg, png, gif的文件')
    else:
        return render_template('user/center.html', user=g.user)

#删除图片
@user_bp1.route('/del_photo')
def del_photo():
    pid = request.args.get('pid')
    photo = Photo.query.get(pid)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('user.user_center'))

#获取图片列表
@user_bp1.route('/myphoto')
def myphoto():
    # 获取文章分类
    types = Article_type.query.all()
    page = int(request.args.get('page', 1))
    photos = Photo.query.paginate(page=page, per_page=3)
    user_id = session.get('uid')
    user = None
    if user_id:
        user = User.query.get(user_id)
    return render_template('user/photo.html', photos=photos, user=user, types=types)


