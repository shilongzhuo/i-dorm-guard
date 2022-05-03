from flask import Blueprint, session, render_template,request
from moudle.rooms import Rooms
room = Blueprint('room',__name__)

@room.route('/room/wec', methods = ['POST', 'GET'])  # 实现缴水电费的界面
def wec():
    roomid = session.get('user')['roomid']
    print('roomid==',roomid)
    room = Rooms().getdata_by_id(roomid)
    if request.method == 'GET':  # GET方式下应当先从数据库中获取宿舍信息
        return render_template('/room/wec.html',room = room)
    else:
        if request.form.get('roommoney_lightlave') != None:
            room.lightlave = int(room.lightlave) + int(request.form.get('roommoney_lightlave'))
            Rooms().update_by_object(room)
        if request.form.get('roommoney_waterlave') != None:
            room.waterlave = int(room.waterlave) + int(request.form.get('roommoney_waterlave'))
            Rooms().update_by_object(room)
        return render_template('/room/wec.html', room=room)