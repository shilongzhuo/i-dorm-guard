from flask import Blueprint, make_response, session, request, render_template, redirect, url_for
from common.utility import ImageCode
from moudle.users import Users
import re

user = Blueprint('user', __name__)


@user.route('/vcode')    # 生成图片验证码
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    print(session.get('code'))
    return response


# 处理登录功能
@user.route('/login', methods=['GET', 'POST'])
def login():
    print('登录A')
    if request.method == 'GET':
        print('登录B')
        return render_template('login.html')
    else:
        print('登录C')
        id = request.form.get('id')
        password = request.form.get('password')
        result = Users().find_by_id_passowrd({'id': id, 'password': password})
        # 登录成功或者失败的判断
        print('id==', id)
        print(password)
        if result and result.isuse == 1:
            print('登录D')
            # 定义一个字典并存入数据
            print('result.id==', result.id)
            userItem = {'id': result.id, 'username': result.username, 'userpic': result.userpic,
                        'roomid': result.roomid, 'petid': result.petid, 'plantid': result.plantid, 'tel': result.tel}

            # session是http协议的状态跟踪技术，http协议是tcp短连接
            session['user'] = userItem
            session['islogin'] = 'true'
            # 登录成功，则保存Cookies信息
            # response = Response(render_template('indexmain',message='登录成功！'))
            # response = Response(redirect('indexmain'))
            # response.set_cookie('username', username, max_age=7 * 24 * 3600)
            # response.set_cookie('password', password, max_age=7 * 24 * 3600)
            # return response
            print(session.get('user'))
            return render_template('index.html', message=userItem)

        else:
            print('登录E')
            return render_template('login.html', message='用户名不存在或密码错误！')


# 处理用户注册
@user.route('/register', methods=['POST'])
def regist():
    print('regist')
    user = Users()
    user.id = request.form.get('regist_id')
    user.password = request.form.get('regist_password')
    user.tel = request.form.get('regist_tel')
    Users().add_user(user)
    return render_template('login.html', message='注册成功')


# 用户退出
@user.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    session['islogin'] = 'false'
    return redirect(url_for('user.login'))


# 用户管理个人信息
@user.route('/profile', methods=['POST', 'GET'])
def profile():
    item = session.get('user')
    user = Users().find_by_id_username({'id': item['id'], 'username': item['username']})
    return render_template('userinfo/profile.html', user=user)


# 用户更新个人信息
@user.route('/updateinfo', methods=['POST', 'GET'])
def updateinfo():
    print('update')
    item = session.get('user')
    user = Users().find_by_id_username({'id': item['id'], 'username': item['username']})
    if request.method == 'GET':
        return render_template('userinfo/updateinfo.html', user=user)
    else:
        print('Hello')
        user.roomid = request.form.get('myupdateroomid')
        user.tel = request.form.get('myupdatetel')
        user.password = request.form.get('myupdatepassword')
        print('password==', user.roomid)
        Users().update_info(user)
        return render_template('userinfo/updateinfo.html', user=user, message='修改成功')


# 用户注销账号
@user.route('/deluser', methods=['POST', 'GET'])
def deluser_try():
    item = session.get('user')
    user = Users().find_by_id_username({'id': item['id'], 'username': item['username']})
    Users().deluser(user)
    session.clear()
    session['islogin'] = 'false'
    return redirect(url_for('user.login'))

# 用户管理宠物界面
@user.route('/pet',methods=['POST','GET'])
def turn_pet():
    item = session.get('user')
    user = Users().find_by_id_username({'id': item['id'], 'username': item['username']})
    return render_template('userinfo/pet.html',user=user)


@user.route('/error',methods=['POST','GET'])
def turn_error():
    item = session.get('user')
    user = Users().find_by_id_username({'id': item['id'], 'username': item['username']})
    return render_template('error.html',user=user)

