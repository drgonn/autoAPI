import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

from app.models.hikv import Hikv



@api.route('/captime/<int:id>', methods=['GET'])
def get_captime(id):
    """get单个定时计划接口

    Params:
        id (int, require): 定时计划ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 定时计划的详细参数
            id (uint optional): 主键ID
            iccid (string optional): 卡iccid
            status (string optional): 通知返回状态码
            created_at (time optional): 创建时间
    """
    captime = Captime.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': captime.to_json(),
                    })


@api.route('/captime', methods=['POST'])
def create_captime():
    """post创建单个定时计划接口

    Requests:
        iccid (string, require): 卡iccid
        status (string, optional): 通知返回状态码

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 定时计划主键ID
    """
    print(request.json)
    iccid = request.json.get('iccid')
    if iccid is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：iccid'})
    status = request.json.get('status')

    captime = Captime(
        iccid=iccid,
        status=status,
    )

    db.session.add(captime)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': captime.id,
                    })


@api.route('/captime/<int:id>', methods=['PUT'])
def modify_captime(id):
    """put修改单个定时计划接口

    Requests:
        iccid (string, optional): 卡iccid
        status (string, optional): 通知返回状态码

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    captime = Captime.query.get_or_404(id)
    iccid = request.json.get('iccid')
    status = request.json.get('status')
    captime.iccid = iccid or captime.iccid
    captime.status = status or captime.status
    db.session.add(captime)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/captime', methods=['DELETE'])
def delete_captime():
    """delete删除多个定时计划接口

    Params:
        ids (list, require): 需要删除的定时计划ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        captime = Captime.query.get(id)
        if captime is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(captime)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/captime/list', methods=['GET'])
def list_captime():
    """get查询定时计划列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        iccid (string optional): 卡iccid，支持模糊匹配,支持排序
        status (string optional): 通知返回状态码,支持精确匹配

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 定时计划的json列表
            id (uint optional): 主键ID
            iccid (string optional): 卡iccid
            status (string optional): 通知返回状态码
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_captimes = Captime.query
    iccid = request.args.get('iccid')
    if iccid is not None:
        total_captimes = total_captimes.filter(Captime.iccid.ilike(f'%{iccid}%'))

    status = request.args.get('status')
    if status is not None:
        total_captimes = total_captimes.filter_by(status=status)

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_captimes = total_captimes.order_by(Captime.id.asc())
        elif sorter.get('id') == 'descend':
            total_captimes = total_captimes.order_by(Captime.id.desc())
        if sorter.get('iccid') == 'ascend':
            total_captimes = total_captimes.order_by(Captime.iccid.asc())
        elif sorter.get('iccid') == 'descend':
            total_captimes = total_captimes.order_by(Captime.iccid.desc())
        if sorter.get('created_at') == 'ascend':
            total_captimes = total_captimes.order_by(Captime.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_captimes = total_captimes.order_by(Captime.created_at.desc())
        pass
    totalcount = total_captimes.with_entities(func.count(Captime.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_captimes.paginate(page, per_page = pageSize, error_out = False)
    captimes = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[captime.to_json() for captime in captimes]
                    })

