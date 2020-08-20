import tushare as ts
import logging
from datetime import timedelta,datetime
import time
from app.models import Stock
from app import db
from time import sleep

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
def update_daily_basic(ts_code=None,trade_date=None,start_date=None,end_date=None):
	print(start_date,end_date)
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







def get_daily(ts_code,start_date,end_date):
	print(start_date,end_date)
	df = pro.daily(ts_code= ts_code,
				   start_date=start_date,
				   end_date=end_date,
				   )
	return df

