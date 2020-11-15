import os
from tools import Tdb


#建立models
def write_auth(root,ojson):
    appname = ojson.get('app')
    initdir = os.path.join(root,f'{appname}/src/app/apiv1/auth.py')
    w = open(initdir,'w+')
    
    auth = ojson.get('auth')

    w.write('from flask import g, jsonify, request\n')
    if auth is not None:
        w.write('from app.tools.auth import untie_token\n')
        w.write('from app.models import User\n')
    w.write('from app.apiv1 import api\n')
    w.write('from app import db\n')
    w.write('#在所有的访问前做token或密码认证\n')
    if auth:
        w.write('@api.before_request\n')
        w.write('def before_request():\n')
        w.write('\ttoken = request.args.get("token")\n')
        w.write('\tif request.endpoint[:8] == "api.test":  # 跳过认证\n')
        w.write('\t\treturn\n')
        w.write('\tif token:\n')
        w.write('\t\ttoken_dir = untie_token(token)\n')
        w.write('\t\tif token_dir.get("error"):\n')
        w.write('''\t\t\treturn jsonify({"success": False, "error_code": 201001, "errmsg": f"{token_dir.get('error')}"}),401\n''')
        w.write('\t\tuid = token_dir["data"].get("uid")\n')
        w.write('\t\trole = token_dir["data"].get("role")\n')
        w.write('\t\tif uid:\n')
        w.write('\t\t\tg.current_user =  User.query.filter_by(uid=uid).first()\n')
        w.write('\t\t\tg.role = role\n')
        w.write('\t\t\tg.token_used = True\n')
        w.write('\t\telse:\n')
        w.write('\t\t\treturn jsonify({"success": False, "error_code": 201001, "errmsg": "token 失效"}),401\n')
        w.write('\t\tif g.current_user is None:\n')
        w.write('\t\t\tuser = User(uid=uid)\n')
        w.write('\t\t\tdb.session.add(user)\n')
        w.write('\t\t\tdb.session.commit()\n')
        w.write('\t\t\tg.current_user = user\n')
        w.write('\telse:\n')
        w.write('\t\treturn jsonify({"success": False, "error_code": -4, "errmsg": "tocken 失效"}),401\n')
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







