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
from app.models import Work,Device

@api.route('/work/<int:id>', methods=['GET'])
def get_work(id):
	work = Work.query.get_or_404(id)

	return jsonify({'success':True,
                    'error_code':0,
                    'records':work.to_json(),
                    })

@api.route('/work', methods=['POST'])
def create_work():
	print(request.json)
	start_time = request.json.get('start_time')
	if start_time is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：start_time'})
	end_time = request.json.get('end_time')
	if end_time is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：end_time'})
	seconds = request.json.get('seconds')
	if seconds is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：seconds'})
	type = request.json.get('type')
	if type is None:
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：type'})

	deviceId = request.json.get('deviceId')
	device = Device.query.filter_by(id=deviceId).first()
 
	if device is None:
		return jsonify({'success':False,'error_code':-1,'errmsg':'deviceId不存在'})	

	work = Work(start_time=start_time,end_time=end_time,seconds=seconds,type=type,device_id=device.id,)

	db.session.add(work)
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'添加数据库发生错误,已经回退:{e}')
		return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/work/<int:id>', methods=['PUT'])
def modify_work(id):
	print('put json:',request.json)
	work = Work.query.get_or_404(id)
	start_time = request.json.get('start_time')
	end_time = request.json.get('end_time')
	seconds = request.json.get('seconds')
	type = request.json.get('type')
	deviceId = request.json.get('deviceId')
	device = Device.query.filter_by(id=deviceId).first()
	if device is None:
		return jsonify({'success':False,'error_code':-1,'errmsg':'deviceId不存在'})	
	work.start_time = start_time or work.start_time
	work.end_time = end_time or work.end_time
	work.seconds = seconds or work.seconds
	work.type = type or work.type
	work.device_id = device.id
	db.session.add(work)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'修改数据库发生错误,已经回退:{e}')
	return jsonify({'success':True,
                    'error_code':0,
                    })

@api.route('/work', methods=['DELETE'])
def delete_work():
	print('delete json:',request.json)
	ids = request.json.get('ids')
	for id in ids:
		work = Work.query.get(id)
		if work is None:
			return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
		db.session.delete(work)

	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error(f'删除数据库发生错误,已经回退:{e}')

	return jsonify({'success':True,
                'error_code':0,
                })

@api.route('/work/list', methods=['GET'])
def list_work():
	print(request.args)
	sorter = request.args.get('sorter')
	page = int(request.args.get('current', 1))
	pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
	pageSize = 20 if pageSize < 10 else pageSize
	total_works = Work.query

	device_id = request.args.get('device_id')
	if device_id is not None:
		device = Device.query.filter_by(id=device_id).first()
		if device is None:
			return jsonify({'success':False,'error_code':-1,'errmsg':'device_id不存在'})
		else:
			total_works = total_works.filter_by(device_id=device.id)
	if sorter:
		sorter = json.loads(sorter)
		pass
	totalcount = total_works.with_entities(func.count(Work.id)).scalar()
	page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
	pagination = total_works.paginate(page, per_page = pageSize, error_out = False)
	works = pagination.items

	return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "pagecount": pagination.pages,
                    'data':[work.to_json() for work in works]
                    })

