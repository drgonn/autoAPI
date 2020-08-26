from datetime import datetime
from flask import g, jsonify,make_response,request, abort, current_app
from app.apiv1 import api
from ..data.tusharedata import  insert_stock,update_last_daily_basic
from app import db
import numpy as np
from app.tools import certify_token,get_trole,certify_token
from ..models import Day,Stock
import time
"""更新数据接口"""


@api.route("/get/all/stocks", methods=["GET"])
def get_all_stocks():
	insert_stock()
	# time.sleep(10)
	return jsonify({
		"success": True,
		"error_code": 0,
		"qrurl" : "order test OK"
	})


@api.route("/update/days", methods=["POST"])
def update_days():
	print(request.json)
	ts_codes = request.json.get('ts_codes')
	#更新所有股票最近一个交易日的数据
	update_all_day= request.json.get('update_all_day')
	if update_all_day:
		update_last_daily_basic()


	# for ts_code in ts_codes:
	# 	df = update_daily_basic(ts_code)



	return jsonify({
		"success": True,
		"error_code": 0,
	})
