import tushare as ts
from app.models import Stock
from app import db
from time import sleep

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


def get_daily_basic(ts_code,start_date,end_date):
	print(start_date,end_date)
	df = pro.daily_basic(ts_code= ts_code,
				   start_date=start_date,
				   end_date=end_date,
				   # fields='ts_code,trade_date,pe,pb,total_mv,circ_mv'
				   )
	return df

def get_daily(ts_code,start_date,end_date):
	print(start_date,end_date)
	df = pro.daily(ts_code= ts_code,
				   start_date=start_date,
				   end_date=end_date,
				   )
	return df
