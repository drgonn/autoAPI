import tushare as ts
import logging
from datetime import timedelta,datetime
import time
from app.models import Stock
from app import db
from time import sleep
from ..models import Day,Stock
import numpy as np

from ..tools.time_way import get_last_unholiday

"""专门从tushare处获取数据的工具"""

token = '2fe78d089caa5a5a5cdc3f9109593fe4a05ba0512acfb5979b54248b'
url = "http://api.waditu.com"

pro = ts.pro_api(token)


def insert_stock():
	print("开始更新所有股票")
	df = pro.query('stock_basic',
				   list_status= 'L',
				   fields = 'ts_code,symbol,name,area, industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
	long = df.index.stop
	for i in range(long):
		d = df.iloc[i]
		print(d)
		if Stock.query.filter_by(ts_code=d.ts_code).first() is not None:
			continue
		print(df['name'][i])

		s = Stock(
			id = int(d.ts_code[:6]),
			ts_code = d.ts_code,
			symbol = d.symbol,
			name  = df['name'][i],
			area  = d.area,
			industry = d.industry,
			fullname = d.fullname,
			# enname =d.enname,
			market=d.market,
			exchange=d.exchange,
			curr_type=d.curr_type,
			list_status=d.list_status,
			list_date=d.list_date,
			delist_date=d.delist_date,
			is_hs=d.is_hs,
		)
		db.session.add(s)
	db.session.commit()
	return df



# 每日指标
def get_daily_basic(ts_code=None,trade_date=None,start_date=None,end_date=None):
	trade_date = trade_date or get_last_unholiday().strftime("%Y%m%d")
	df = pro.daily_basic(ts_code= ts_code,
						 trade_date = trade_date,
				   start_date=start_date,
				   end_date=end_date,
				   # fields='ts_code,trade_date,pe,pb,total_mv,circ_mv'
				   )
	c = 0
	while df.empty and c <10:
		c += 1
		trade_date = (datetime.strptime(trade_date,"%Y%m%d")-timedelta(days=1)).strftime("%Y%m%d")
		df = pro.daily_basic(ts_code= ts_code,
							 trade_date = trade_date,
							 start_date=start_date,
							 end_date=end_date,
							 )
	if df.empty:
		logging.error("tusharedata 发生更新错误，超过10天都找不到最近的数据，可能是停牌了")

	return df
# 更新某只股票的所有日数据
def update_stock_daily_basic(ts_code):
	df = pro.daily_basic(ts_code= ts_code,
						 )
	long = df.index.stop
	stock = Stock.query.filter_by(ts_code=ts_code).first()
	if stock is None:
		logging.error(f'更新所有股票的最近一个交易日数据过程当中stock:{ts_code}没有找到')
	# for i in range(long):
	for i in range(10):
		d = df.iloc[i]
		if Day.query.filter_by(stock=stock).filter_by(trade_date=d.trade_date).first() is not None:
			print(f'stock:{d.ts_code}已经存在')
			continue
		s = Day(
			stock_id=stock.id,
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



# 更新所有股票的最近一个交易日数据
def update_last_daily_basic():
	logging.info("开始更新每日数据了")
	df = get_daily_basic()
	long = df.index.stop
	for i in range(long):
		d = df.iloc[i]
		stock = Stock.query.filter_by(ts_code=d.ts_code).first()
		if stock is None:
			logging.error(f'更新所有股票的最近一个交易日数据过程当中stock:{d.ts_code}没有找到')
			continue
		if Day.query.filter_by(stock=stock).filter_by(trade_date=d.trade_date).first() is not None:
			print(f'stock:{d.ts_code}已经存在')
			continue

		s = Day(
			stock_id=stock.id,
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


def get_daily(ts_code,start_date,end_date):
	print(start_date,end_date)
	df = pro.daily(ts_code= ts_code,
				   start_date=start_date,
				   end_date=end_date,
				   )
	return df

