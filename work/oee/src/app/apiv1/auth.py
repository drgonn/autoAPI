from datetime import datetime
from flask import g, jsonify,make_response,request, abort, current_app
from app.apiv1 import api
from app import db
from app.tools import certify_token,get_trole,certify_token
#在所有的访问前做token或密码认证
@api.teardown_request
def teardown_request(exception=None):
	db.session.close()

@api.route("/test", methods=["GET"])
def test():
	return jsonify({
		"success": True,
		"error_code": 0,
		"qrurl" : "order test OK"
	})
