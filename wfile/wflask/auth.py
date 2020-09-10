import os
from tools import Tdb


#建立models
def write_auth(root,ojson):
    appname = ojson.get('app')
    initdir = os.path.join(root,f'{appname}/src/app/apiv1/auth.py')
    w = open(initdir,'w+')
    
    auth = ojson.get('auth')

    w.write('from datetime import datetime\n')
    w.write('from flask import g, jsonify,make_response,request, abort, current_app\n')
    if auth is not None:
        w.write('from app.models import User, Permission\n')
    w.write('from app.apiv1 import api\n')
    w.write('from app import db\n')
    w.write('from app.tools import certify_token,get_trole,certify_token\n')
    w.write('#在所有的访问前做token或密码认证\n')
    if auth is not None:
        w.write('@api.before_request\n')
        w.write('def before_request():\n')
        w.write('\ttoken = request.args.get("token")\n')
        w.write('\tif request.endpoint[:8] == "api.test":  # 跳过认证\n')
        w.write('\t\treturn\n')
        w.write('\tif token:\n')
        w.write('\t\tuid = certify_token(token).get("uid")\n')
        w.write('\t\tappKey = certify_token(token).get("appKey")\n')
        w.write('\t\tuserapp = App.query.filter_by(key=appKey).first() if appKey is not None else None\n')
        w.write('\t\tif userapp is None:\n')
        w.write('\t\t\treturn jsonify({"success": False, "error_code": 201001, "errmsg": "缺少app，appKey错误"})\n')
        w.write('\t\tif not userapp.activate:\n')
        w.write('\t\t\treturn jsonify({"success": False, "error_code": 201001, "errmsg": "您的服务已经停用，请检查是否是到期"})\n')
        w.write('\t\tg.app = userapp\n')
        w.write('\t\tif uid:\n')
        w.write('\t\t\tg.current_user =  User.query.filter_by(uid=uid).first()\n')
        w.write('\t\t\tg.role = get_trole(token)\n')
        w.write('\t\t\tg.token_used = True\n')
        w.write('\t\telse:\n')
        w.write('\t\t\treturn jsonify({"success": False, "error_code": 201001, "errmsg": "token 失效"})\n')
        w.write('\t\tif g.current_user is None:\n')
        w.write('\t\t\tuser = User(uid=uid)\n')
        w.write('\t\t\tdb.session.add(user)\n')
        w.write('\t\t\tdb.session.commit()\n')
        w.write('\t\t\tg.current_user = user\n')
        w.write('\telse:\n')
        w.write('\t\treturn jsonify({"success": False, "error_code": -4, "errmsg": "tocken 失效"})\n')
    w.write('@api.teardown_request\n')
    w.write('def teardown_request(exception=None):\n')
    w.write('\tdb.session.close()\n')
    w.write('\n')
    w.write('@api.route("/test", methods=["GET"])\n')
    w.write('def test():\n')
    w.write('\treturn jsonify({\n')
    w.write('\t\t"success": True,\n')
    w.write('\t\t"error_code": 0,\n')
    w.write('\t\t"qrurl" : "order test OK"\n')
    w.write('\t})\n')
    w.close()






