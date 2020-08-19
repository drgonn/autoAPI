from datetime import datetime
from flask import g, jsonify,make_response,request, abort, current_app
from app.apiv1 import api
from app.data.tusharedata import  insert_stock
from app import db
from app.tools import certify_token,get_trole,certify_token
import time
"""更新数据接口"""


@api.route("/get/all/stocks", methods=["GET"])
def get_all_stocks():
	insert_stock()
	# time.sleep(10)
	return jsonify({
		"ret": True,
		"error_code": 0,
		"qrurl" : "order test OK"
	})
