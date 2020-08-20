from datetime import datetime
from flask import g, jsonify,make_response,request, abort, current_app
from app.apiv1 import api
from app.data.tusharedata import  insert_stock,update_daily_basic
from app import db
from app.tools import certify_token,get_trole,certify_token
from ..models import Day
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


@api.route("/update/days", methods=["POST"])
def update_days():
	print(request.json)
	ts_codes = request.json.get('ts_codes')
	#更新所有股票最近一个交易日的数据
	update_all_day= request.json.get('update_all_day')
	if update_all_day:
		df = update_daily_basic()
		long = df.index.stop
		for i in range(long):
			d = df.iloc[i]
			print(d)
			# if Day.query.filter_by(ts_code=d.ts_code).first() is not None:
			# 	continue
			# print(df['name'][i])

		# 	s = Day(
        #         stock = stock,
		# 		symbol = d.symbol,
		# 		name  = df['name'][i],
		# 		area  = d.area,
		# 		industry = d.industry,
		# 		fullname = d.fullname,
		# 		# enname =d.enname,
		# 		market=d.market,
		# 		exchange=d.exchange,
		# 		curr_type=d.curr_type,
		# 		list_status=d.list_status,
		# 		list_date=d.list_date,
		# 		delist_date=d.delist_date,
		# 		is_hs=d.is_hs,
		# 	)
		# 	db.session.add(s)
		# db.session.commit()

	# for ts_code in ts_codes:
	# 	df = update_daily_basic(ts_code)

	return jsonify({
		"ret": True,
		"error_code": 0,
	})
