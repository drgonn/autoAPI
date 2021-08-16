from app import db
from app.apiv1 import api
from flask import jsonify, request
import time
from datetime import datetime,date,timedelta

from ..data.tusharedata import insert_stock,insert_index,  update_stock_daily_basic, update_index_daily
# from ..data.akshareData import insert_stock, update_last_daily_basic, update_stock_daily_basic
from ..models import Day, Stock, Group,Index,Indexday,Score
from ..tools.trade_date import buydate
import numpy as np
from functools import reduce


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
			print(stock)
			print(stock.days.first())
			if stock.days.first() is not None:
				continue
		d = stock.days.order_by(Day.trade_date.desc()).first()
		if d:
			start_date = d.trade_date
			print(start_date,date.today())
			if start_date >= date.today() -timedelta(days=1):
				print(f'要更新的日期是{start_date},就是今天，已经有最新数据，无需更新')
				continue
			start_date = datetime.strftime(start_date, "%Y%m%d")
		else:
			start_date = None
		print("开始获取时间",start_date,stock.name,stock.ts_code)
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
		print("开始获取时间",start_date,index.name,index.ts_code)
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



@api.route("/fill/days", methods=["GET"])
def fill_days():
	"""计算所有股票的涨跌幅度"""
	stocks = Stock.query.filter(Stock.id > 992)
	for stock in stocks:
		"""计算过去一年的收益结果存起来,最后一天的收益率，或指定天的收益"""
		group = Group.query.filter_by(name = stock.industry).filter_by(type=2).first()
		if not group:
			return jsonify({
				"success": False,
				"error_code": -1,
				"errmsg":f"{stock.name}没有行业",
			})
		stock.groups.append(group)

		print(stock.name,stock.id)
		group_id= stock.groups.filter_by(type=2).first().id
		print(stock.groups.filter_by(type=2).first().name)
		cl = list()
		for d in stock.days.order_by(Day.trade_date.asc()):
			# print(f'{d.trade_date}的收盘价是： {d.close}')
			if len(cl) >1:
				d.pct1 = (d.close/cl[-1]) - 1
			# print(f'单日涨幅{d.pct1}')
			if len(cl) >3:
				d.pct3 = (d.close/cl[-3]) - 1
			# print(f'3日涨幅{d.pct3}')
			if len(cl) >5:
				d.pct5 = (d.close/cl[-5]) - 1
			# print(f'5日涨幅{d.pct5}')
			if len(cl) >10:
				d.pct10 = (d.close/cl[-10]) - 1
			# print(f'10日涨幅{d.pct5}')
			if len(cl) >20:
				d.pct20 = (d.close/cl[-20]) - 1
				# print(f'20日涨幅{d.pct20}')
				cl.pop(0)
			d.group_id = group_id
			cl.append(d.close)
			db.session.add(d)
		db.session.commit()
	return jsonify({
		"success": True,
		"error_code": 0,
	})

from .temp import income_way2
@api.route("/simulation/test", methods=["POST"])
def simulation():
	"""模拟测试打印，临时测试用"""
	# print("先找股票的中位数")
	# stocks = Stock.query.all()
	stocks = Group.query.get(25).stocks.all()
	tian = 300
	for stock in stocks:
		days = stock.days.all()
		start_p = days[0].close
		close_p = days[-1].close
		l = len(days)
		# print(days[:10])
		# z = len(days)//2
		print(f"{stock.name}拿着不动，最开始时间是{days[0].trade_date}，价格{start_p}，结束时间是{days[-1].trade_date}，价格{close_p}，平均收益{(close_p/start_p)/l}，收益:            {close_p/start_p}")
		buy_price = 0
		fes = []
		if l <tian:
			break
		for i,d in enumerate(days[tian:]):
			if d.pe:
				ndays = days[i:tian+i]
				pes = [d.pe for d in ndays]
				pes = list(filter(None, pes))
				z = np.median(pes)
				# print(f"\n{stock.name}的市盈利中位数是{z}")
				if d.pe < z and buy_price == 0:
					buy_price = d.close
				elif d.pe > z and buy_price != 0:
					fe = d.close/buy_price
					buy_price = 0
					fes.append(fe)
		sum = reduce(lambda x, y: x * y, fes)
		print(f"中位数计算方法，收益比例是{len(fes)},收益倍数是:                                                 {sum}")






	# print("开始按照两数当中的大数为上，小数为下，获取大小两数，超过大数卖出，低于小数买入。")

	print("")
	print("")
	# j2 = Score.query.filter_by(score_type_id=2).filter_by(trade_date="20210107").order_by(Score.score.desc()).limit(100).all()
	# j2 = [j.stock.name for j in j2]
	# j3 = Score.query.filter_by(score_type_id=3).filter_by(trade_date="20210107").order_by(Score.score.desc()).limit(100).all()
	# j3 = [j.stock.name for j in j3]
	# j4 = Score.query.filter_by(score_type_id=4).filter_by(trade_date="20210107").order_by(Score.score.desc()).limit(100).all()
	# j4 = [j.stock.name for j in j4]
	# j5 = Score.query.filter_by(score_type_id=5).filter_by(trade_date="20210107").order_by(Score.score.desc()).limit(100).all()
	# j5 = [j.stock.name for j in j5]
	#
	# j = list(set(j2)& set(j3) & set(j4) & set(j5) )
	# print(j)
	#
	# """
	# 一批股票，先计算每股五年盈利，然后计算平均盈利，然后计算算法盈利
	# """
	# endday = "20201229"
	# startday = "20180108"
	# avl = []
	# for i in j:
	# 	print(i)
	# 	stock = Stock.query.filter_by(name=i).first()
	# 	end = stock.days.order_by(Day.trade_date.desc()).filter(Day.trade_date >=endday).first()
	# 	start = stock.days.order_by(Day.trade_date.asc()).filter(Day.trade_date >=startday).first()
	# 	print(end.close,start.close)
	# 	avl.append(end.close/start.close)
	# avange = sum(avl)/len(j)
	# print("计算得平均值是",avange)
	#
	# # 循环日期,从大盘开始
	# datel = buydate(startday,endday)
	# stocks = Stock.query.filter(Stock.name.in_(j)).all()
	# stock_ids = [s.id for s in stocks]
	# print(stocks)
	# buystocks = {}
	# for i in stocks:
	# 	buystocks[i.name] = {"mount":0,"price":0}
	#
	# length = len(j)
	# half = length//2
	# divid = 100/half
	# remain = 0
	# # 第一天，买入前跌幅最高一半股票
	# for d in datel:
	# 	days = Day.query.filter(Day.stock_id.in_(stock_ids)).filter_by(trade_date=d).all()
	# 	sds  = days.sort(key = lambda x : x.pct1)
	# 	print([i.pct1 for i in days[::-1]])
	# 	for i in days[:half]:
	# 		buystocks[i.stock.name]['mount'] = divid
	# 		buystocks[i.stock.name]['price'] = i.close
	# 	# print(buystocks)
	# 	break
	# for d in datel:
	# 	days = Day.query.filter(Day.stock_id.in_(stock_ids)).filter_by(trade_date=d).all()
	# 	# print([i.pct1 for i in days])
	# 	sds  = days.sort(key = lambda x : x.pct1)
	# 	# 找到跌幅最高没有买入股票，买入，涨幅最高的持仓股，卖掉
	# 	for i in days[::-1]:
	# 		if buystocks[i.stock.name]['mount'] != 0:
	# 			mount = buystocks[i.stock.name]['mount']
	# 			buystocks[i.stock.name]['mount'] = 0
	# 			buyprice = buystocks[i.stock.name]['price']
	# 			li = i.close/buyprice
	# 			remain = mount* li
	# 			break
	# 	for i in days:
	# 		if buystocks[i.stock.name]['mount'] == 0:
	# 			buystocks[i.stock.name]['mount'] = remain
	# 			buystocks[i.stock.name]['price'] = i.close
	# 			remain = 0
	# 			break
	# 	break
	# buystocks = {'泸州老窖': {'mount': 0, 'price': 192.25}, '酒鬼酒': {'mount': 0, 'price': 119.13}, '高德红外': {'mount': 158.90997379455337, 'price': 41.75}, '亿纬锂能': {'mount': 0, 'price': 72.27}, '新宙邦': {'mount': 64.67662345076965, 'price': 104.0}, '汇川技术': {'mount': 71.58909111349267, 'price': 90.9}, '片仔癀': {'mount': 0, 'price': 227.3}, '通威股份': {'mount': 0, 'price': 30.02}, '通策医疗': {'mount': 71.93156359820635, 'price': 260.31}, '山西汾酒': {'mount': 117.538043872948, 'price': 321.25}, '妙可蓝多': {'mount': 49.569339594788865, 'price': 45.93}, '中国中免': {'mount': 0, 'price': 217.25}}
	#
	#
	# rall = sum([value['mount'] for value in buystocks.values()])
	# print(rall/100)








	return jsonify({
		"success": True,
		"error_code": 0,
	})
