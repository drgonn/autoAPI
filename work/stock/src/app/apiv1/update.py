from app import db
from app.apiv1 import api
from flask import jsonify, request
import time
from datetime import datetime

from ..data.tusharedata import insert_stock,insert_index,  update_stock_daily_basic, update_index_daily
# from ..data.akshareData import insert_stock, update_last_daily_basic, update_stock_daily_basic
from ..models import Day, Stock, Group,Index,Indexday

"""更新数据接口"""

@api.route("/get/all/stocks", methods=["GET"])
def get_all_stocks():
	"""拉取所有stock的基本信息"""
	insert_stock()
	return jsonify({
		"success": True,
		"error_code": 0,
	})

@api.route("/get/all/index", methods=["GET"])
def get_all_index():
	"""拉取所有Index指标的基本信息"""
	insert_index()
	return jsonify({
		"success": True,
		"error_code": 0,
	})

@api.route("/update/days", methods=["POST"])
def update_days():
	""" 根据参数更新所有股票最近一个stock股票交易日的数据"""
	print(request.json)
	ts_codes = request.json.get('ts_codes')
	empty = request.json.get('empty')   #补齐所有日线为空的股票
	update_all_day= request.json.get('update_all_day')

	if update_all_day:
		stocks = Stock.query
	elif ts_codes:
		stocks = Stock.query.filter(Stock.ts_code.in_(ts_codes))

	if not stocks:
		return ({"success": False, "error_code": -2, "errmsg": f'stock {ts_codes} 为空或找不到'})

	for stock in stocks:
		if empty:
			if stock.days.first() is not None:
				continue
		d = stock.days.order_by(Day.trade_date.desc()).first()
		if d:
			start_date = d.trade_date
			start_date = datetime.strftime(start_date, "%Y%m%d")
		else:
			start_date = None
		print("开始获取时间",start_date,stock.name)
		update_stock_daily_basic(stock,start_date)
		time.sleep(1)


	return jsonify({
		"success": True,
		"error_code": 0,
	})

@api.route("/update/index/daily", methods=["POST"])
def update_index_days():
	""" 根据参数更新所有股票最近一个index指标交易日的数据"""
	print(request.json)
	ts_codes = request.json.get('ts_codes')
	update_all_day = request.json.get('update_all_day')

	if update_all_day:
		indexs = Index.query.filter(Index.about != None)
	elif ts_codes:
		indexs = Index.query.filter(Index.ts_code.in_(ts_codes))

	if not indexs:
		return ({"success": False, "error_code": -2, "errmsg": f'index {ts_codes} 为空或找不到'})

	for index in indexs:
		print(index)
		d = index.indexdays.order_by(Indexday.trade_date.desc()).first()
		if d:
			start_date = d.trade_date
			start_date = datetime.strftime(start_date, "%Y%m%d")
		else:
			start_date = None
		print("开始获取时间",start_date,index.name)
		update_index_daily(index,start_date)

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
	""""""
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

