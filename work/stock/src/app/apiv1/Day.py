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
	trade_date = request.json.get('trade_date')
	if trade_date is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：trade_date'})
	close = request.json.get('close')
	if close is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：close'})
	turnover_rate = request.json.get('turnover_rate')
	if turnover_rate is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：turnover_rate'})
	turnover_rate_f = request.json.get('turnover_rate_f')
	if turnover_rate_f is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：turnover_rate_f'})
	volume_ratio = request.json.get('volume_ratio')
	if volume_ratio is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：volume_ratio'})
	pe = request.json.get('pe')
	if pe is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：pe'})
	pe_ttm = request.json.get('pe_ttm')
	if pe_ttm is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：pe_ttm'})
	pb = request.json.get('pb')
	if pb is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：pb'})
	ps = request.json.get('ps')
	if ps is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：ps'})
	ps_ttm = request.json.get('ps_ttm')
	if ps_ttm is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：ps_ttm'})
	dv_ratio = request.json.get('dv_ratio')
	if dv_ratio is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：dv_ratio'})
	dv_ttm = request.json.get('dv_ttm')
	if dv_ttm is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：dv_ttm'})
	total_share = request.json.get('total_share')
	if total_share is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：total_share'})
	float_share = request.json.get('float_share')
	if float_share is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：float_share'})
	free_share = request.json.get('free_share')
	if free_share is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：free_share'})
	total_mv = request.json.get('total_mv')
	if total_mv is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：total_mv'})
	circ_mv = request.json.get('circ_mv')
	if circ_mv is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：circ_mv'})

	stockId = request.json.get('stockId')
	stock = Stock.query.filter_by(id=stockId).first()
 
	if stock is None:
		return jsonify({'success':False,'error_code':-1,'errmsg':'stockId不存在'})	

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
	stockId = request.json.get('stockId')
	stock = Stock.query.filter_by(id=stockId).first()
	if stock is None:
		return jsonify({'success':False,'error_code':-1,'errmsg':'stockId不存在'})	
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

@api.route('/day/<int:id>', methods=['DELETE'])
def delete_day(id):
	day = Day.query.get_or_404(id)
	db.session.delete(day)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'删除数据库发生错误,已经回退:{e}')

	return jsonify({'success':True,
                'error_code':0,
                })

@api.route('/day/list', methods=['POST'])
def list_day():
	print(request.json)
	order = request.json.get('order')
	sorter = request.json.get('sorter')
	page = int(request.json.get('current', 1))
	pagesize = int(request.json.get('pagesize', current_app.config['PER_PAGE']))
	pagesize = 20 if pagesize < 10 else pagesize
	total_days = Day.query

	stockId = request.json.get('stockId')
	if stockId is not None:
		stock = Stock.query.filter_by(id=stockId).first()
		if stock is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':'stockId不存在'})
		else:
			total_days = total_days.filter_by(stock_id=stock.id)

	trade_date = request.json.get('trade_date')
	if trade_date is not None:
		total_days = total_days.filter_by(trade_date=trade_date)
	if sorter:
		if sorter.get('trade_date')== 'ascend':
			total_days = total_days.order_by(Day.trade_date.asc())
		if sorter.get('trade_date')== 'descend':
			total_days = total_days.order_by(Day.trade_date.desc())
	if sorter:
		if sorter.get('close')== 'ascend':
			total_days = total_days.order_by(Day.close.asc())
		if sorter.get('close')== 'descend':
			total_days = total_days.order_by(Day.close.desc())
	if sorter:
		if sorter.get('turnover_rate')== 'ascend':
			total_days = total_days.order_by(Day.turnover_rate.asc())
		if sorter.get('turnover_rate')== 'descend':
			total_days = total_days.order_by(Day.turnover_rate.desc())
	if sorter:
		if sorter.get('turnover_rate_f')== 'ascend':
			total_days = total_days.order_by(Day.turnover_rate_f.asc())
		if sorter.get('turnover_rate_f')== 'descend':
			total_days = total_days.order_by(Day.turnover_rate_f.desc())
	if sorter:
		if sorter.get('volume_ratio')== 'ascend':
			total_days = total_days.order_by(Day.volume_ratio.asc())
		if sorter.get('volume_ratio')== 'descend':
			total_days = total_days.order_by(Day.volume_ratio.desc())
	if sorter:
		if sorter.get('pe')== 'ascend':
			total_days = total_days.order_by(Day.pe.asc())
		if sorter.get('pe')== 'descend':
			total_days = total_days.order_by(Day.pe.desc())
	if sorter:
		if sorter.get('pe_ttm')== 'ascend':
			total_days = total_days.order_by(Day.pe_ttm.asc())
		if sorter.get('pe_ttm')== 'descend':
			total_days = total_days.order_by(Day.pe_ttm.desc())
	if sorter:
		if sorter.get('pb')== 'ascend':
			total_days = total_days.order_by(Day.pb.asc())
		if sorter.get('pb')== 'descend':
			total_days = total_days.order_by(Day.pb.desc())
	if sorter:
		if sorter.get('ps')== 'ascend':
			total_days = total_days.order_by(Day.ps.asc())
		if sorter.get('ps')== 'descend':
			total_days = total_days.order_by(Day.ps.desc())
	if sorter:
		if sorter.get('ps_ttm')== 'ascend':
			total_days = total_days.order_by(Day.ps_ttm.asc())
		if sorter.get('ps_ttm')== 'descend':
			total_days = total_days.order_by(Day.ps_ttm.desc())
	if sorter:
		if sorter.get('dv_ratio')== 'ascend':
			total_days = total_days.order_by(Day.dv_ratio.asc())
		if sorter.get('dv_ratio')== 'descend':
			total_days = total_days.order_by(Day.dv_ratio.desc())
	if sorter:
		if sorter.get('dv_ttm')== 'ascend':
			total_days = total_days.order_by(Day.dv_ttm.asc())
		if sorter.get('dv_ttm')== 'descend':
			total_days = total_days.order_by(Day.dv_ttm.desc())
	if sorter:
		if sorter.get('total_share')== 'ascend':
			total_days = total_days.order_by(Day.total_share.asc())
		if sorter.get('total_share')== 'descend':
			total_days = total_days.order_by(Day.total_share.desc())
	if sorter:
		if sorter.get('float_share')== 'ascend':
			total_days = total_days.order_by(Day.float_share.asc())
		if sorter.get('float_share')== 'descend':
			total_days = total_days.order_by(Day.float_share.desc())
	if sorter:
		if sorter.get('free_share')== 'ascend':
			total_days = total_days.order_by(Day.free_share.asc())
		if sorter.get('free_share')== 'descend':
			total_days = total_days.order_by(Day.free_share.desc())
	if sorter:
		if sorter.get('total_mv')== 'ascend':
			total_days = total_days.order_by(Day.total_mv.asc())
		if sorter.get('total_mv')== 'descend':
			total_days = total_days.order_by(Day.total_mv.desc())
	if sorter:
		if sorter.get('circ_mv')== 'ascend':
			total_days = total_days.order_by(Day.circ_mv.asc())
		if sorter.get('circ_mv')== 'descend':
			total_days = total_days.order_by(Day.circ_mv.desc())
	totalcount = total_days.with_entities(func.count(Day.id)).scalar()
	page = math.ceil(totalcount/pagesize) if  math.ceil(totalcount/pagesize) < page else page
	pagination = total_days.paginate(page, per_page = pagesize, error_out = False)
	days = pagination.items

	return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    'data':[day.to_json() for day in days]
                    })

