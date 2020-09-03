from datetime import date,timedelta,datetime
import logging
import math
import json

from flask import request,jsonify,current_app,g
from sqlalchemy import func
from sqlalchemy import not_,or_,and_,extract

from app.apiv1 import api
from app.standard import Permission
from app.decorators import admin_required, permission_required
from app import db
from app.tools import is_admin,get_permission
from app.models import Stock,Group

@api.route('/stock/<int:id>', methods=['GET'])
def get_stock(id):
	stock = Stock.query.get_or_404(id)

	return jsonify({'success':True,
                    'error_code':0,
                    'records':stock.to_json(),
                    })

@api.route('/stock', methods=['POST'])
def create_stock():
	print(request.json)
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

	group_ids = request.json.get('group_ids') or []
	for group_id in group_ids:
		group = Group.query.filter_by(id=group_id)
		if group is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':'groupID不存在'})
		stock.groups.append(group)
	

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
	print('put json:',request.json)
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

	add_group_ids = request.json.get('add_group_ids')
	if add_group_ids:
		original_ids = [group.id for group in stock.groups.all()]
		new_ids = list(set(add_group_ids).difference(set(original_ids)))
		for group_id in new_ids:
			group = Group.query.filter_by(id=group_id).first()
			if group is None:
				return jsonify({'success':False,'error_code':-1,'errmsg':'groupID不存在'})
			stock.groups.append(group)

	remove_group_ids = request.json.get('remove_group_ids')
	if remove_group_ids:
		original_ids = [group.id for group in stock.groups.all()]
		remove_ids = list(set(remove_group_ids).intersection(set(original_ids)))
		for group_id in remove_ids:
			group = Group.query.filter_by(id=group_id).first()
			stock.groups.remove(group)
		
	db.session.add(stock)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'修改数据库发生错误,已经回退:{e}')
	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/stock', methods=['DELETE'])
def delete_stock():
	print('delete json:',request.json)
	ids = request.json.get('ids')
	for id in ids:
		stock = Stock.query.get(id)
		if stock is None:
			return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
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

@api.route('/stock/list', methods=['GET'])
def list_stock():
	print(request.args)
	sorter = request.args.get('sorter')
	page = int(request.args.get('current', 1))
	pagesize = int(request.args.get('pagesize', current_app.config['PER_PAGE']))
	pagesize = 20 if pagesize < 10 else pagesize
	total_stocks = Stock.query

	group_id = request.args.get('group_id')
	if group_id is not None:
		group = Group.query.filter_by(id=group_id).first()
		if group is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':f'group:{group_id}不存在'})
		else:
			total_stocks = group.stocks

	ts_code = request.args.get('ts_code')
	if ts_code is not None:
		total_stocks = total_stocks.filter(Stock.ts_code.ilike(f'%{ts_code}%'))

	symbol = request.args.get('symbol')
	if symbol is not None:
		total_stocks = total_stocks.filter(Stock.symbol.ilike(f'%{symbol}%'))

	if sorter:
		sorter = json.loads(sorter)
		if sorter.get('list_date') == 'ascend':
			total_stocks = total_stocks.order_by(Stock.list_date.asc())
		elif sorter.get('list_date') == 'descend':
			total_stocks = total_stocks.order_by(Stock.list_date.desc())
		pass
	totalcount = total_stocks.with_entities(func.count(Stock.id)).scalar()
	page = math.ceil(totalcount/pagesize) if  math.ceil(totalcount/pagesize) < page else page
	pagination = total_stocks.paginate(page, per_page = pagesize, error_out = False)
	stocks = pagination.items

	return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pagesize" : pagesize,
                    "pagecount": pagination.pages,
                    'data':[stock.to_json() for stock in stocks]
                    })

