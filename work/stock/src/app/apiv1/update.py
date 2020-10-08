from datetime import datetime
from flask import g, jsonify,make_response,request, abort, current_app
from app.apiv1 import api
from ..data.tusharedata import  insert_stock,update_last_daily_basic,update_stock_daily_basic
from app import db
import numpy as np
from app.tools import certify_token,get_trole,certify_token
from ..models import Day,Stock,Group
import time
"""更新数据接口"""

# 拉取最早的所有股票
@api.route("/get/all/stocks", methods=["GET"])
def get_all_stocks():
	insert_stock()
	# time.sleep(10)
	return jsonify({
		"success": True,
		"error_code": 0,
		"qrurl" : "order test OK"
	})


# 更新所有股票最近一个交易日的数据
@api.route("/update/days", methods=["POST"])
def update_days():
	print(request.json)
	ts_codes = request.json.get('ts_codes')
	#更新所有股票最近一个交易日的数据
	update_all_day= request.json.get('update_all_day')
	if update_all_day:
		update_last_daily_basic()
	elif ts_codes:
		for ts_code in ts_codes:
			update_stock_daily_basic(ts_code)

	return jsonify({
		"success": True,
		"error_code": 0,
	})

@api.route("/scores/<statu>", methods=["GET"])
def scores(statu):
	# 计算行业排名得分
	if statu == "new":
		industry_new_score()
	elif statu == "all":
		industry_all_score()
	else:
		return jsonify({
			"success": False,
			"error_code": -1,
			"errmsg":"更新状态不对，有new和all",
		})

	return jsonify({
		"success": True,
		"error_code": 0,
	})

def industry_new_score():
	groups = Group.query.filter_by(type=2).all()
	for group in groups:
		ds = []
		for stock in  group.stocks:
			d = stock.days.order_by(Day.trade_date.desc()).first()
			if d:
				ds.append(d)
		dsmv = [d.total_mv for d in ds]
		total_mv = sum(dsmv)
		for d in ds:
			d.score = (d.total_mv/total_mv)*100
			if d.score is not None:
				d.stock.score = d.score
			db.session.add(d)
		db.session.commit()


def industry_all_score():
	groups = Group.query.filter_by(type=2).all()
	for group in groups:
		if group.stocks.first() is None:
			continue
		stock1 = group.stocks[0]
		for td in stock1.days:
			trade_date = td.trade_date
			ds = []
			for stock in group.stocks:
				d = stock.days.filter_by(trade_date=trade_date).first()
				if d:
					ds.append(d)
			dsmv = [d.total_mv for d in ds]
			total_mv = sum(dsmv)
			for d in ds:
				d.score = (d.total_mv/total_mv)*100
				if d.score is not None:
					d.stock.score = d.score
				db.session.add(d)
			db.session.commit()





def indus():
	stocks = Stock.query.all()
	for stock in stocks:
		industry = stock.industry
		group = Group.query.filter_by(name=industry).first()
		if 'ST' in stock.name:
			continue
		if group:
			group.type = 2
			group.stocks.append(stock)
			if 'ST' in stock.name:
				group.stocks.remove(stock)
		else:
			group = Group(name=industry,type=2)
			# group.stocks.append(stock)

		db.session.add(group)
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(f'添加数据库发生错误,已经回退:{e}')
		# return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

