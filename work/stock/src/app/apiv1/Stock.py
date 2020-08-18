from datetime import date,timedelta,datetime
import logging
import math

from flask import request,jsonify,current_app,g
from sqlalchemy import func
from sqlalchemy import not_,or_,and_,extract

from app.apiv1 import api
from app.standard import Permission
from app.decorators import admin_required, permission_required
from app import db
from app.tools import is_admin,get_permission
from app.models import Stock

@api.route('/stock/<int:id>', methods=['GET'])
def get_stock(id):
	stock = Stock.query.get_or_404(id)

	return jsonify({'success':True,
                    'error_code':0,
                    'records':stock.to_json(),
                    })



@api.route('/stock', methods=['POST'])
def create_stock():
	ts_code = request.json.get('ts_code')
	if ts_code is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：ts_code'})
	symbol = request.json.get('symbol')
	if symbol is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：symbol'})
	name = request.json.get('name')
	if name is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
	area = request.json.get('area')
	if area is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：area'})
	industry = request.json.get('industry')
	if industry is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：industry'})
	fullname = request.json.get('fullname')
	if fullname is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：fullname'})
	enname = request.json.get('enname')
	if enname is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：enname'})
	market = request.json.get('market')
	if market is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：market'})
	exchange = request.json.get('exchange')
	if exchange is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：exchange'})
	curr_type = request.json.get('curr_type')
	if curr_type is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：curr_type'})
	list_status = request.json.get('list_status')
	if list_status is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：list_status'})
	list_date = request.json.get('list_date')
	if list_date is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：list_date'})
	delist_date = request.json.get('delist_date')
	if delist_date is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：delist_date'})
	is_hs = request.json.get('is_hs')
	if is_hs is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：is_hs'})
	price = request.json.get('price')
	if price is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：price'})

	stock = Stock(ts_code=ts_code,symbol=symbol,name=name,area=area,industry=industry,fullname=fullname,enname=enname,market=market,exchange=exchange,curr_type=curr_type,list_status=list_status,list_date=list_date,delist_date=delist_date,is_hs=is_hs,price=price,)

	db.session.add(stock)
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'添加数据库发生错误,已经回退:{e}')
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/stock/<int:id>', methods=['PUT'])
def modify_stock(id):
	stock = Stock.query.get_or_404(id)
	ts_code = request.json.get('ts_code')
	symbol = request.json.get('symbol')
	name = request.json.get('name')
	area = request.json.get('area')
	industry = request.json.get('industry')
	fullname = request.json.get('fullname')
	enname = request.json.get('enname')
	market = request.json.get('market')
	exchange = request.json.get('exchange')
	curr_type = request.json.get('curr_type')
	list_status = request.json.get('list_status')
	list_date = request.json.get('list_date')
	delist_date = request.json.get('delist_date')
	is_hs = request.json.get('is_hs')
	price = request.json.get('price')
	stock.ts_code = ts_code or stock.ts_code
	stock.symbol = symbol or stock.symbol
	stock.name = name or stock.name
	stock.area = area or stock.area
	stock.industry = industry or stock.industry
	stock.fullname = fullname or stock.fullname
	stock.enname = enname or stock.enname
	stock.market = market or stock.market
	stock.exchange = exchange or stock.exchange
	stock.curr_type = curr_type or stock.curr_type
	stock.list_status = list_status or stock.list_status
	stock.list_date = list_date or stock.list_date
	stock.delist_date = delist_date or stock.delist_date
	stock.is_hs = is_hs or stock.is_hs
	stock.price = price or stock.price
	db.session.add(stock)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'修改数据库发生错误,已经回退:{e}')
	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/stock/<int:id>', methods=['DELETE'])
def delete_stock(id):
	stock = Stock.query.get_or_404(id)
	db.session.delete(stock)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'删除数据库发生错误,已经回退:{e}')

	return jsonify({'success':True,
                'error_code':0,
                })

@api.route('/stock/list', methods=['POST'])
def list_stock():
	print(request.json)
	order = request.json.get('order')
	sorter = request.json.get('sorter')
	page = int(request.json.get('current', 1))
	pagesize = int(request.json.get('pagesize', current_app.config['PER_PAGE']))
	pagesize = 20 if pagesize < 10 else pagesize
	total_stocks = Stock.query

	ts_code = request.json.get('ts_code')
	if ts_code is not None:
		total_stocks = total_stocks.filter_by(ts_code=ts_code)
	if sorter:
		if sorter.get('ts_code')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.ts_code.asc())
		if sorter.get('ts_code')== 'descend':
			total_stocks = total_stocks.order_by(Stock.ts_code.desc())

	symbol = request.json.get('symbol')
	if symbol is not None:
		total_stocks = total_stocks.filter_by(symbol=symbol)
	if sorter:
		if sorter.get('symbol')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.symbol.asc())
		if sorter.get('symbol')== 'descend':
			total_stocks = total_stocks.order_by(Stock.symbol.desc())

	name = request.json.get('name')
	if name is not None:
		total_stocks = total_stocks.filter_by(name=name)
	if sorter:
		if sorter.get('name')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.name.asc())
		if sorter.get('name')== 'descend':
			total_stocks = total_stocks.order_by(Stock.name.desc())

	area = request.json.get('area')
	if area is not None:
		total_stocks = total_stocks.filter_by(area=area)
	if sorter:
		if sorter.get('area')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.area.asc())
		if sorter.get('area')== 'descend':
			total_stocks = total_stocks.order_by(Stock.area.desc())

	industry = request.json.get('industry')
	if industry is not None:
		total_stocks = total_stocks.filter_by(industry=industry)
	if sorter:
		if sorter.get('industry')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.industry.asc())
		if sorter.get('industry')== 'descend':
			total_stocks = total_stocks.order_by(Stock.industry.desc())

	fullname = request.json.get('fullname')
	if fullname is not None:
		total_stocks = total_stocks.filter_by(fullname=fullname)
	if sorter:
		if sorter.get('fullname')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.fullname.asc())
		if sorter.get('fullname')== 'descend':
			total_stocks = total_stocks.order_by(Stock.fullname.desc())

	enname = request.json.get('enname')
	if enname is not None:
		total_stocks = total_stocks.filter_by(enname=enname)
	if sorter:
		if sorter.get('enname')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.enname.asc())
		if sorter.get('enname')== 'descend':
			total_stocks = total_stocks.order_by(Stock.enname.desc())

	market = request.json.get('market')
	if market is not None:
		total_stocks = total_stocks.filter_by(market=market)
	if sorter:
		if sorter.get('market')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.market.asc())
		if sorter.get('market')== 'descend':
			total_stocks = total_stocks.order_by(Stock.market.desc())

	exchange = request.json.get('exchange')
	if exchange is not None:
		total_stocks = total_stocks.filter_by(exchange=exchange)
	if sorter:
		if sorter.get('exchange')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.exchange.asc())
		if sorter.get('exchange')== 'descend':
			total_stocks = total_stocks.order_by(Stock.exchange.desc())

	curr_type = request.json.get('curr_type')
	if curr_type is not None:
		total_stocks = total_stocks.filter_by(curr_type=curr_type)
	if sorter:
		if sorter.get('curr_type')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.curr_type.asc())
		if sorter.get('curr_type')== 'descend':
			total_stocks = total_stocks.order_by(Stock.curr_type.desc())

	list_status = request.json.get('list_status')
	if list_status is not None:
		total_stocks = total_stocks.filter_by(list_status=list_status)
	if sorter:
		if sorter.get('list_status')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.list_status.asc())
		if sorter.get('list_status')== 'descend':
			total_stocks = total_stocks.order_by(Stock.list_status.desc())

	list_date = request.json.get('list_date')
	if list_date is not None:
		total_stocks = total_stocks.filter_by(list_date=list_date)
	if sorter:
		if sorter.get('list_date')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.list_date.asc())
		if sorter.get('list_date')== 'descend':
			total_stocks = total_stocks.order_by(Stock.list_date.desc())

	delist_date = request.json.get('delist_date')
	if delist_date is not None:
		total_stocks = total_stocks.filter_by(delist_date=delist_date)
	if sorter:
		if sorter.get('delist_date')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.delist_date.asc())
		if sorter.get('delist_date')== 'descend':
			total_stocks = total_stocks.order_by(Stock.delist_date.desc())

	is_hs = request.json.get('is_hs')
	if is_hs is not None:
		total_stocks = total_stocks.filter_by(is_hs=is_hs)
	if sorter:
		if sorter.get('is_hs')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.is_hs.asc())
		if sorter.get('is_hs')== 'descend':
			total_stocks = total_stocks.order_by(Stock.is_hs.desc())
	if sorter:
		if sorter.get('price')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.price.asc())
		if sorter.get('price')== 'descend':
			total_stocks = total_stocks.order_by(Stock.price.desc())
	totalcount = total_stocks.with_entities(func.count(Stock.id)).scalar()
	page = math.ceil(totalcount/pagesize) if  math.ceil(totalcount/pagesize) < page else page
	pagination = total_stocks.paginate(page, per_page = pagesize, error_out = False)
	stocks = pagination.items

	return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    'data':[stock.to_json() for stock in stocks]
                    })

