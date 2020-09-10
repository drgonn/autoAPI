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
from app.models import Group,Stock

@api.route('/group/<int:id>', methods=['GET'])
def get_group(id):
	group = Group.query.get_or_404(id)

	return jsonify({'success':True,
                    'error_code':0,
                    'records':group.to_json(),
                    })

@api.route('/group', methods=['POST'])
def create_group():
	print(request.json)
	name = request.json.get('name')

	group = Group(name=name,)

	stock_ids = request.json.get('stock_ids') or []
	for stock_id in stock_ids:
		stock = Stock.query.filter_by(id=stock_id)
		if stock is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':'stockID不存在'})
		group.stocks.append(stock)
	

	db.session.add(group)
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'添加数据库发生错误,已经回退:{e}')
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/group/<int:id>', methods=['PUT'])
def modify_group(id):
	print('put json:',request.json)
	group = Group.query.get_or_404(id)
	name = request.json.get('name')
	group.name = name or group.name

	add_stock_ids = request.json.get('add_stock_ids')
	if add_stock_ids:
		original_ids = [stock.id for stock in group.stocks.all()]
		new_ids = list(set(add_stock_ids).difference(set(original_ids)))
		for stock_id in new_ids:
			stock = Stock.query.filter_by(id=stock_id).first()
			if stock is None:
				return jsonify({'success':False,'error_code':-1,'errmsg':'stockID不存在'})
			group.stocks.append(stock)

	remove_stock_ids = request.json.get('remove_stock_ids')
	if remove_stock_ids:
		original_ids = [stock.id for stock in group.stocks.all()]
		remove_ids = list(set(remove_stock_ids).intersection(set(original_ids)))
		for stock_id in remove_ids:
			stock = Stock.query.filter_by(id=stock_id).first()
			group.stocks.remove(stock)
		
	db.session.add(group)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'修改数据库发生错误,已经回退:{e}')
	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/group', methods=['DELETE'])
def delete_group():
	print('delete json:',request.json)
	ids = request.json.get('ids')
	for id in ids:
		group = Group.query.get(id)
		if group is None:
			return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
	db.session.delete(group)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'删除数据库发生错误,已经回退:{e}')

	return jsonify({'success':True,
                'error_code':0,
                })

@api.route('/group/list', methods=['GET'])
def list_group():
	print(request.args)
	sorter = request.args.get('sorter')
	page = int(request.args.get('current', 1))
	pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
	pageSize = 20 if pageSize < 10 else pageSize
	total_groups = Group.query

	stock_id = request.args.get('stock_id')
	if stock_id is not None:
		stock = Stock.query.filter_by(id=stock_id).first()
		if stock is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':f'stock:{stock_id}不存在'})
		else:
			total_groups = stock.groups

	name = request.args.get('name')
	if name is not None:
		total_groups = total_groups.filter(Group.name.ilike(f'%{name}%'))

	if sorter:
		sorter = json.loads(sorter)
		pass
	totalcount = total_groups.with_entities(func.count(Group.id)).scalar()
	page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
	pagination = total_groups.paginate(page, per_page = pageSize, error_out = False)
	groups = pagination.items

	return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "pagecount": pagination.pages,
                    'data':[group.to_json() for group in groups]
                    })

