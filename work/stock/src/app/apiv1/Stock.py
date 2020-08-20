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
	if stock.days.first() is not None:
		return jsonify({'success':False,'error_code':-1,'errmsg':'stock还拥有day，不能删除'})
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
	# print(request.json)
	order = request.json.get('order')
	sorter = request.json.get('sorter')
	page = int(request.json.get('current', 1))
	pagesize = int(request.json.get('pagesize', current_app.config['PER_PAGE']))
	pagesize = 20 if pagesize < 10 else pagesize
	total_stocks = Stock.query

	stockId = request.json.get('stockId')
	if stockId is not None:
		stock = Stock.query.filter_by(id=stockId).first()
		if stock is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':'stockId不存在'})
		else:
			total_stocks = total_stocks.filter_by(stock_id=stock.id)

	trade_date = request.json.get('trade_date')
	if trade_date is not None:
		total_stocks = total_stocks.filter_by(trade_date=trade_date)
	if sorter:
		if sorter.get('trade_date')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.trade_date.asc())
		if sorter.get('trade_date')== 'descend':
			total_stocks = total_stocks.order_by(Stock.trade_date.desc())
	if sorter:
		if sorter.get('close')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.close.asc())
		if sorter.get('close')== 'descend':
			total_stocks = total_stocks.order_by(Stock.close.desc())
	if sorter:
		if sorter.get('turnover_rate')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.turnover_rate.asc())
		if sorter.get('turnover_rate')== 'descend':
			total_stocks = total_stocks.order_by(Stock.turnover_rate.desc())
	if sorter:
		if sorter.get('turnover_rate_f')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.turnover_rate_f.asc())
		if sorter.get('turnover_rate_f')== 'descend':
			total_stocks = total_stocks.order_by(Stock.turnover_rate_f.desc())
	if sorter:
		if sorter.get('volume_ratio')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.volume_ratio.asc())
		if sorter.get('volume_ratio')== 'descend':
			total_stocks = total_stocks.order_by(Stock.volume_ratio.desc())
	if sorter:
		if sorter.get('pe')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.pe.asc())
		if sorter.get('pe')== 'descend':
			total_stocks = total_stocks.order_by(Stock.pe.desc())
	if sorter:
		if sorter.get('pe_ttm')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.pe_ttm.asc())
		if sorter.get('pe_ttm')== 'descend':
			total_stocks = total_stocks.order_by(Stock.pe_ttm.desc())
	if sorter:
		if sorter.get('pb')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.pb.asc())
		if sorter.get('pb')== 'descend':
			total_stocks = total_stocks.order_by(Stock.pb.desc())
	if sorter:
		if sorter.get('ps')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.ps.asc())
		if sorter.get('ps')== 'descend':
			total_stocks = total_stocks.order_by(Stock.ps.desc())
	if sorter:
		if sorter.get('ps_ttm')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.ps_ttm.asc())
		if sorter.get('ps_ttm')== 'descend':
			total_stocks = total_stocks.order_by(Stock.ps_ttm.desc())
	if sorter:
		if sorter.get('dv_ratio')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.dv_ratio.asc())
		if sorter.get('dv_ratio')== 'descend':
			total_stocks = total_stocks.order_by(Stock.dv_ratio.desc())
	if sorter:
		if sorter.get('dv_ttm')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.dv_ttm.asc())
		if sorter.get('dv_ttm')== 'descend':
			total_stocks = total_stocks.order_by(Stock.dv_ttm.desc())
	if sorter:
		if sorter.get('total_share')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.total_share.asc())
		if sorter.get('total_share')== 'descend':
			total_stocks = total_stocks.order_by(Stock.total_share.desc())
	if sorter:
		if sorter.get('float_share')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.float_share.asc())
		if sorter.get('float_share')== 'descend':
			total_stocks = total_stocks.order_by(Stock.float_share.desc())
	if sorter:
		if sorter.get('free_share')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.free_share.asc())
		if sorter.get('free_share')== 'descend':
			total_stocks = total_stocks.order_by(Stock.free_share.desc())
	if sorter:
		if sorter.get('total_mv')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.total_mv.asc())
		if sorter.get('total_mv')== 'descend':
			total_stocks = total_stocks.order_by(Stock.total_mv.desc())
	if sorter:
		if sorter.get('circ_mv')== 'ascend':
			total_stocks = total_stocks.order_by(Stock.circ_mv.asc())
		if sorter.get('circ_mv')== 'descend':
			total_stocks = total_stocks.order_by(Stock.circ_mv.desc())
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

