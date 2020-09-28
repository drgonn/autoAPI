
import json
import logging
import math

from app import db
from app.apiv1 import api
from app.models import Day, Stock
from flask import request, jsonify, current_app
from sqlalchemy import func

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
	circ_mv = request.json.get('circ_mv')
	pe = request.json.get('pe')
	score = request.json.get('score')

	stock = Stock(ts_code=ts_code,symbol=symbol,name=name,area=area,industry=industry,fullname=fullname,enname=enname,market=market,exchange=exchange,curr_type=curr_type,list_status=list_status,list_date=list_date,delist_date=delist_date,is_hs=is_hs,price=price,circ_mv=circ_mv,pe=pe,score=score,)

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
	circ_mv = request.json.get('circ_mv')
	pe = request.json.get('pe')
	score = request.json.get('score')
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
	stock.circ_mv = circ_mv or stock.circ_mv
	stock.pe = pe or stock.pe
	stock.score = score or stock.score

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
			return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

	return jsonify({'success':True,
                'error_code':0,
                })

@api.route('/stock/list', methods=['GET'])
def list_stock():
	print(request.args)
	sorter = request.args.get('sorter')
	page = int(request.args.get('current', 1))
	pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
	pageSize = 20 if pageSize < 10 else pageSize
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

	name = request.args.get('name')
	if name is not None:
		total_stocks = total_stocks.filter(Stock.name.ilike(f'%{name}%'))

	if sorter:
		sorter = json.loads(sorter)
		if sorter.get('industry') == 'ascend':
			total_stocks = total_stocks.order_by(Stock.industry.asc())
		elif sorter.get('industry') == 'descend':
			total_stocks = total_stocks.order_by(Stock.industry.desc())
		if sorter.get('list_date') == 'ascend':
			total_stocks = total_stocks.order_by(Stock.list_date.asc())
		elif sorter.get('list_date') == 'descend':
			total_stocks = total_stocks.order_by(Stock.list_date.desc())
		if sorter.get('price') == 'ascend':
			total_stocks = total_stocks.order_by(Stock.price.asc())
		elif sorter.get('price') == 'descend':
			total_stocks = total_stocks.order_by(Stock.price.desc())
		if sorter.get('circ_mv') == 'ascend':
			total_stocks = total_stocks.order_by(Stock.circ_mv.asc())
		elif sorter.get('circ_mv') == 'descend':
			total_stocks = total_stocks.order_by(Stock.circ_mv.desc())
		if sorter.get('pe') == 'ascend':
			total_stocks = total_stocks.order_by(Stock.pe.asc())
		elif sorter.get('pe') == 'descend':
			total_stocks = total_stocks.order_by(Stock.pe.desc())
		if sorter.get('score') == 'ascend':
			total_stocks = total_stocks.order_by(Stock.score.asc())
		elif sorter.get('score') == 'descend':
			total_stocks = total_stocks.order_by(Stock.score.desc())
		pass
	totalcount = total_stocks.with_entities(func.count(Stock.id)).scalar()
	page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
	pagination = total_stocks.paginate(page, per_page = pageSize, error_out = False)
	stocks = pagination.items

	return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[stock.to_json() for stock in stocks]
                    })

