from datetime import datetime
from flask import g, jsonify,make_response,request, abort, current_app
from app.apiv1 import api
from app.data.tusharedata import  insert_stock,update_daily_basic
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
		df = update_daily_basic()
		long = df.index.stop
		for i in range(long):
			d = df.iloc[i]
			stock = Stock.query.filter_by(ts_code=d.ts_code).first()
			if stock is None:
				return jsonify({'success': False, 'error_code': -123, 'errmsg': f'stock:{d.ts_code}没有找到'})
			if Day.query.filter_by(stock=stock).filter_by(trade_date=d.trade_date).first() is not None:
				print(f'stock:{d.ts_code}已经存在')
				continue

			s = Day(
                stock_id = stock.id,
				trade_date=d.trade_date,
				close=np.float(d.close) if not np.isnan(d.close) else None,
				turnover_rate=np.float(d.turnover_rate) if not np.isnan(d.turnover_rate) else None,
				turnover_rate_f=np.float(d.turnover_rate_f) if not np.isnan(d.turnover_rate_f) else None,
				volume_ratio=np.float(d.volume_ratio) if not np.isnan(d.volume_ratio) else None,
				pe=np.float(d.pe) if not np.isnan(d.pe) else None,
				pe_ttm=np.float(d.pe_ttm) if not np.isnan(d.pe_ttm) else None,
				pb=np.float(d.pb) if not np.isnan(d.pb) else None,
				ps=np.float(d.ps) if not np.isnan(d.ps) else None,
				ps_ttm=np.float(d.ps_ttm) if not np.isnan(d.ps_ttm) else None,
				dv_ratio=np.float(d.dv_ratio) if not np.isnan(d.dv_ratio) else None,
				dv_ttm=np.float(d.dv_ttm) if not np.isnan(d.dv_ttm) else None,
				total_share=np.float(d.total_share) if not np.isnan(d.total_share) else None,
				float_share=np.float(d.float_share) if not np.isnan(d.float_share) else None,
				free_share=np.float(d.free_share) if not np.isnan(d.free_share) else None,
				total_mv=np.float(d.total_mv) if not np.isnan(d.total_mv) else None,
				circ_mv=np.float(d.circ_mv) if not np.isnan(d.circ_mv) else None,
			)
			db.session.add(s)
			db.session.commit()

	# for ts_code in ts_codes:
	# 	df = update_daily_basic(ts_code)



	return jsonify({
		"success": True,
		"error_code": 0,
	})
