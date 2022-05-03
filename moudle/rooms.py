from sqlalchemy import Table

from common.database import dbconnect

dbsession, md, DBase = dbconnect()

class Rooms(DBase):
    __table__ = Table('rooms', md, autoload=True)

    # 根据宿舍id获取宿舍信息
    def getdata_by_id(self,roomid):
        row = dbsession.query(Rooms).filter(Rooms.id == roomid).first()
        return row
    # 跟据提交的对象对room表中的数据进行更新
    def update_by_object(self,oj):
        room = dbsession.query(Rooms).filter(Rooms.id == oj.id).first()
        room = oj
        dbsession.commit()