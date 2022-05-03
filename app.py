import os
from datetime import timedelta
import pymysql
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
#from demo_cam import start_monitoring

pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)  # 使用session时用到
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的过期时间为7天
# 使用集成方式处理SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zhuoshilong@localhost:3306/i-dormguard?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True:跟踪数据库的修改，及时发送信号
app.config['SQLALCHEMY_POOL_SIZE'] = 100  # 数据库连接池的大小。默认是数据库引擎的默认值（通常是 5）

# 实例化db对象
db = SQLAlchemy(app)


# 定义404错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html')


# 定义500错误页面
@app.errorhandler(500)
def internal_error(e):
    return render_template('error-500.html')


# 针对app实例定义全局拦截器(全局拦截器不好，不能什么都拦截，那么网页就没有办法访问了)
@app.before_request
def before():
    # 如果用户已经登录session['islogin']='true',则不作拦截
    url = request.path  # 读取到当前接口的地址
    # 静态资源如图片，CSS和JS代码等，可以通过后缀名来进行放行
    pass_list = ['/login', '/register', '/test', '/vcode','/room/wec','/notice_board']
    suffix = url.endswith('.png') or url.endswith('.jpg') or url.endswith('.css') or url.endswith('.jpeg') or url.endswith(
        '.js') or url.endswith('.min.js')
    if url in pass_list or suffix:
        pass  # 如果在白名单中，则执行请求，不做拦截
    elif session.get('islogin') != 'true':  # 没登录的话先返回到登录界面
        print('请先登录')
        return render_template('login.html')
    else:
        pass


if __name__ == '__main__':
    # 开启人脸识别
    # start_monitoring()

    # 为了避免循环引用，注册蓝图的代码必须放到main函数中
    from controller.user import *

    app.register_blueprint(user)  # 注册user的蓝图

    from controller.index import *

    app.register_blueprint(index)  # 注册index的蓝图

    from  controller.room import *
    app.register_blueprint(room)   # 注册room的蓝图

    from controller.video import *

    app.register_blueprint(video)  # 注册video的蓝图

    from controller.notice import *

    app.register_blueprint(notice)  # 注册notice的蓝图

    app.run(debug=True)
