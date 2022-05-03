from sqlalchemy import Table

from common.database import dbconnect

dbsession, md, DBase = dbconnect()


class Users(DBase):
    __table__ = Table('users', md, autoload=True)

    # 根据学号和密码查询特定用户
    def find_by_id_passowrd(self, id):
        row = dbsession.query(Users).filter(Users.id == id['id'], Users.password == id['password']).first()
        print('AAAAAAA==', row)
        return row

        # 根据学号和姓名查询特定用户

    def find_by_id_username(self, id):
        row = dbsession.query(Users).filter(Users.id == id['id'], Users.username == id['username']).first()
        print('BBBBBBB==', row)
        return row

    # 新增用户(新增用户前要判断用户是否已经存在)
    # 注册时传过来的应当是一个字典:{user_id:xxx, user_name:xxx, password:xxx,...}
    def add_user(self, id):
        print('id.id==', id.id)
        user = dbsession.query(Users).filter(Users.id == id.id, Users.password == id.password).first()
        print(user.tel)
        user.tel = id.tel
        user.isuse = 1  # 表明这个用户已经使用这个服务了，即注册
        dbsession.commit()

    # 用户信息更新
    def update_info(self, id):
        user = dbsession.query(Users).filter(Users.id == id.id).first()
        user.roomid = id.roomid
        user.tel = id.tel
        user.password = id.password
        dbsession.commit()

    # 用户注销账号
    def deluser(self, id):
        user = dbsession.query(Users).filter(Users.id == id.id).first()
        user.password = user.id
        user.isuse = 0  # 表明这个用户停止使用服务，即注销账号
        dbsession.commit()
