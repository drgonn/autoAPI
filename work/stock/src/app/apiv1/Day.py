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
from app.models import Day,Stock

@api.route('/day/<int:id>', methods=['GET'])
def get_day(id):
	day = Day.query.get_or_404(id)

	return jsonify({'success':True,
                    'error_code':0,
                    'records':day.to_json(),
                    })

@api.route('/day', methods=['POST'])
def create_day():
	print(request.json)
	trade_date = request.json.get('trade_date')
	close = request.json.get('close')
	turnover_rate = request.json.get('turnover_rate')
	turnover_rate_f = request.json.get('turnover_rate_f')
	volume_ratio = request.json.get('volume_ratio')
	pe = request.json.get('pe')
	pe_ttm = request.json.get('pe_ttm')
	pb = request.json.get('pb')
	ps = request.json.get('ps')
	ps_ttm = request.json.get('ps_ttm')
	dv_ratio = request.json.get('dv_ratio')
	dv_ttm = request.json.get('dv_ttm')
	total_share = request.json.get('total_share')
	float_share = request.json.get('float_share')
	free_share = request.json.get('free_share')
	total_mv = request.json.get('total_mv')
	circ_mv = request.json.get('circ_mv')

	stock_id = request.json.get('stock_id')
	stock = Stock.query.filter_by(id=stock_id).first()
 
	if stock is None:
		return jsonify({'success':False,'error_code':-1,'errmsg':'stock_id不存在'})	

	day = Day(trade_date=trade_date,close=close,turnover_rate=turnover_rate,turnover_rate_f=turnover_rate_f,volume_ratio=volume_ratio,pe=pe,pe_ttm=pe_ttm,pb=pb,ps=ps,ps_ttm=ps_ttm,dv_ratio=dv_ratio,dv_ttm=dv_ttm,total_share=total_share,float_share=float_share,free_share=free_share,total_mv=total_mv,circ_mv=circ_mv,stock_id=stock.id,)

	db.session.add(day)
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'添加数据库发生错误,已经回退:{e}')
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/day/<int:id>', methods=['PUT'])
def modify_day(id):
	print('put json:',request.json)
	day = Day.query.get_or_404(id)
	trade_date = request.json.get('trade_date')
	close = request.json.get('close')
	turnover_rate = request.json.get('turnover_rate')
	turnover_rate_f = request.json.get('turnover_rate_f')
	volume_ratio = request.json.get('volume_ratio')
	pe = request.json.get('pe')
	pe_ttm = request.json.get('pe_ttm')
	pb = request.json.get('pb')
	ps = request.json.get('ps')
	ps_ttm = request.json.get('ps_ttm')
	dv_ratio = request.json.get('dv_ratio')
	dv_ttm = request.json.get('dv_ttm')
	total_share = request.json.get('total_share')
	float_share = request.json.get('float_share')
	free_share = request.json.get('free_share')
	total_mv = request.json.get('total_mv')
	circ_mv = request.json.get('circ_mv')
	stock_id = request.json.get('stock_id')
	stock = Stock.query.filter_by(id=stock_id).first()
	if stock is None:
		return jsonify({'success':False,'error_code':-1,'errmsg':'stock_id不存在'})	
	day.trade_date = trade_date or day.trade_date
	day.close = close or day.close
	day.turnover_rate = turnover_rate or day.turnover_rate
	day.turnover_rate_f = turnover_rate_f or day.turnover_rate_f
	day.volume_ratio = volume_ratio or day.volume_ratio
	day.pe = pe or day.pe
	day.pe_ttm = pe_ttm or day.pe_ttm
	day.pb = pb or day.pb
	day.ps = ps or day.ps
	day.ps_ttm = ps_ttm or day.ps_ttm
	day.dv_ratio = dv_ratio or day.dv_ratio
	day.dv_ttm = dv_ttm or day.dv_ttm
	day.total_share = total_share or day.total_share
	day.float_share = float_share or day.float_share
	day.free_share = free_share or day.free_share
	day.total_mv = total_mv or day.total_mv
	day.circ_mv = circ_mv or day.circ_mv
	day.stock_id = stock.id
	db.session.add(day)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'修改数据库发生错误,已经回退:{e}')
	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/day', methods=['DELETE'])
def delete_day():
	print('delete json:',request.json)
	ids = request.json.get('ids')
	for id in ids:
		day = Day.query.get(id)
		if day is None:
			return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
	db.session.delete(day)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'删除数据库发生错误,已经回退:{e}')

	return jsonify({'success':True,
                'error_code':0,
                })

@api.route('/day/list', methods=['GET'])
def list_day():
	print(request.args)
	sorter = request.args.get('sorter')
	page = int(request.args.get('current', 1))
	pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
	pageSize = 20 if pageSize < 10 else pageSize
	total_days = Day.query

	stock_id = request.args.get('stock_id')
	if stock_id is not None:
		stock = Stock.query.filter_by(id=stock_id).first()
		if stock is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':'stock_id不存在'})
		else:
			total_days = total_days.filter_by(stock_id=stock.id)
	if sorter:
		sorter = json.loads(sorter)
		if sorter.get('ps_ttm') == 'ascend':
			total_days = total_days.order_by(Day.ps_ttm.asc())
		elif sorter.get('ps_ttm') == 'descend':
			total_days = total_days.order_by(Day.ps_ttm.desc())
		if sorter.get('dv_ratio') == 'ascend':
			total_days = total_days.order_by(Day.dv_ratio.asc())
		elif sorter.get('dv_ratio') == 'descend':
			total_days = total_days.order_by(Day.dv_ratio.desc())
		if sorter.get('dv_ttm') == 'ascend':
			total_days = total_days.order_by(Day.dv_ttm.asc())
		elif sorter.get('dv_ttm') == 'descend':
			total_days = total_days.order_by(Day.dv_ttm.desc())
		if sorter.get('total_share') == 'ascend':
			total_days = total_days.order_by(Day.total_share.asc())
		elif sorter.get('total_share') == 'descend':
			total_days = total_days.order_by(Day.total_share.desc())
		if sorter.get('float_share') == 'ascend':
			total_days = total_days.order_by(Day.float_share.asc())
		elif sorter.get('float_share') == 'descend':
			total_days = total_days.order_by(Day.float_share.desc())
		if sorter.get('free_share') == 'ascend':
			total_days = total_days.order_by(Day.free_share.asc())
		elif sorter.get('free_share') == 'descend':
			total_days = total_days.order_by(Day.free_share.desc())
		if sorter.get('total_mv') == 'ascend':
			total_days = total_days.order_by(Day.total_mv.asc())
		elif sorter.get('total_mv') == 'descend':
			total_days = total_days.order_by(Day.total_mv.desc())
		if sorter.get('circ_mv') == 'ascend':
			total_days = total_days.order_by(Day.circ_mv.asc())
		elif sorter.get('circ_mv') == 'descend':
			total_days = total_days.order_by(Day.circ_mv.desc())
		pass
	totalcount = total_days.with_entities(func.count(Day.id)).scalar()
	page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
	pagination = total_days.paginate(page, per_page = pageSize, error_out = False)
	days = pagination.items

	return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "pagecount": pagination.pages,
                    'data':[day.to_json() for day in days]
                    })

