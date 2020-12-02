#!-*- coding:utf-8 -*-
__author__ = 'ALX LIN'
from flask import Blueprint,request, render_template,redirect,url_for
from apps.user.models import User
from exts import db
import hashlib
from sqlalchemy import or_,and_
user_bp = Blueprint('user', __name__)


#用户注册
@user_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        if password == repassword:
            #与模型结合,拿取属性的值
            #1.找到模型类并创建对象
            user = User()
            #2.给对象的属性赋值
            user.username = username
            user.password = hashlib.md5(password.encode('utf-8')).hexdigest()
            user.phone = phone
            #添加数据至数据库
            #3.将user对象添加到session（）中【缓存】
            db.session.add(user)
            #4.将缓存的数据插入到数据库里，提交数据
            db.session.commit()
            return redirect(url_for('user.user_center'))
        else:
            return "二次密码不一致"
    return render_template('user/register.html')

#用户中心
@user_bp.route('/', methods=['GET', 'POST'])
def user_center():
    #查询数据库中的数据
    users = User.query.filter(User.isdelete == False).all() #select * from user;
    print(users) #[user_objA, user_objB] 返回的是数据对象
    return render_template('user/center.html', users=users)

#用户登陆
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    #获取输入的用户名和密码
    if request.method == 'POST':
        username = request.form.get('username')
        password = hashlib.md5(request.form.get('password').encode('utf-8')).hexdigest()
        #获取数据库里的数据，与账号密码匹配
        # users = User.query.all()
        #for循环验证账号密码
        # for user in users:
        #     if username == user.username and password == user.password:
        #         return redirect(url_for('user.user_center'))
        #     else:
        #         print("账号或密码错误")
        #数据库查询验证账号
        user_list = User.query.filter_by(username=username)
        us = User.query.filter(User.username==username)
        print('1', user_list)
        print('2', us)
        for u in user_list:
            if u.password == password:
                return '用户登陆成功'
        else:
            return render_template('user/login.html', msg='用户名或密码错误')

    return render_template('user/login.html')

#用户搜索
@user_bp.route('/search')
def search():
    keyqord = request.args.get('search')
    user_list = User.query.filter(or_(User.username.contains(keyqord), User.phone.contains(keyqord))).all()
    return render_template('user/center.html', users=user_list)

#测试路由
@user_bp.route('/test')
def test():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    print(user)
    return 'test'

@user_bp.route('/select')
def user_select():
    user = User.query.get(4) #根据主键查询用户使用get（主键值）返回值是一个用户对象
    print('query_byde1显示',user,type(user))
    user1 = User.query.filter(User.username == 'jack').all()
    user2 = User.query.filter(User.username.startswith('j')).all()
    user3 = User.query.filter(User.username.endswith('n')).all()
    # user4 = User.query.filter(User.username.contains('ac')).all()
    # print("测试时",user4[1], type(user4))
    #查询或条件
    user4 = User.query.filter(or_(User.username.like('z%'), User.username.like('%i%')).all())
    #查询且条件
    user5 = User.query.filter(and_(User.username.like('z%'), User.username.like('%i%')).all())
    #排序
    user6 = User.query.filter(User.username.contains('%s%')).order_by('rdatatime').all()#升序
    user6 = User.query.filter(User.username.contains('%s%')).order_by(-User.ratatime).all()#降序

    #限制使用 limit offest
    user8 = User.query.limit(2).all()
    user8 = User.query.offset(2).limit(2).all()

    return render_template('user/select.html', user2=user4)


#用户删除
@user_bp.route('/delete', endpoint='delete')
def user_delete():
    #获取用户id
    id = request.args.get('id')
    #获取该id的用户
    user = User.query.get(id)
    #逻辑删除
    user.isdelete = True
    #提交
    db.session.commit()
    #2.物理删除
    # user = User.query.get(id)
    # #将对象放到缓存准备删除
    # db.session.delete(user)
    # db.session.commit()
    return redirect(url_for('user.user_center'))

#用户信息更新
@user_bp.route('/update', endpoint='update', methods=['POST', 'GET'])
def user_update():
    if request.method == 'POST':
        id = request.form.get('id')
        username = request.form.get('username')
        phone = request.form.get('phone')
        #找用户
        user = User.query.get(id)
        #修改用户的信息
        user.phone = phone
        user.username = username
        #提交
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        id = request.args.get('id')
        user = User.query.get(id)
        return render_template('user/update.html', users=user)
