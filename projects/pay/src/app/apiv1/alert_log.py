import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

from app.models.alert import Alert



@api.route('/alert_log/<int:id>', methods=['GET'])
def get_alert_log(id):
    """get单个告警日志接口

    Params:
        id (int, require): 告警日志ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 告警日志的详细参数
            id (uint optional): 主键ID
            iccid (string optional): 名称
            status (int optional): 状态, 1可激活, 2已激活, 3已停用
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    alert_log = AlertLog.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': alert_log.to_json(),
                    })


@api.route('/alert_log', methods=['POST'])
def create_alert_log():
    """post创建单个告警日志接口

    Requests:
        iccid (string, require): 名称

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 告警日志主键ID
    """
    print(request.json)
    iccid = request.json.get('iccid')
    if iccid is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：iccid'})

    alert_log = AlertLog(
        iccid=iccid,
    )

    db.session.add(alert_log)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': alert_log.id,
                    })


@api.route('/alert_log/<int:id>', methods=['PUT'])
def modify_alert_log(id):
    """put修改单个告警日志接口

    Requests:
        iccid (string, optional): 名称

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    alert_log = AlertLog.query.get_or_404(id)
    iccid = request.json.get('iccid')
    alert_log.iccid = iccid or alert_log.iccid
    db.session.add(alert_log)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/alert_log', methods=['DELETE'])
def delete_alert_log():
    """delete删除多个告警日志接口

    Params:
        ids (list, require): 需要删除的告警日志ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        alert_log = AlertLog.query.get(id)
        if alert_log is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(alert_log)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/alert_log/list', methods=['GET'])
def list_alert_log():
    """get查询告警日志列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        iccid (string optional): 名称，支持模糊匹配,支持排序
        status (int optional): 状态,支持精确匹配, 1可激活, 2已激活, 3已停用

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 告警日志的json列表
            id (uint optional): 主键ID
            iccid (string optional): 名称
            status (int optional): 状态, 1可激活, 2已激活, 3已停用
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_alert_logs = AlertLog.query
    iccid = request.args.get('iccid')
    if iccid is not None:
        total_alert_logs = total_alert_logs.filter(AlertLog.iccid.ilike(f'%{iccid}%'))

    status = request.args.get('status')
    if status is not None:
        total_alert_logs = total_alert_logs.filter_by(status=status)

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.id.asc())
        elif sorter.get('id') == 'descend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.id.desc())
        if sorter.get('iccid') == 'ascend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.iccid.asc())
        elif sorter.get('iccid') == 'descend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.iccid.desc())
        if sorter.get('updated_at') == 'ascend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_alert_logs = total_alert_logs.order_by(AlertLog.created_at.desc())
        pass
    totalcount = total_alert_logs.with_entities(func.count(AlertLog.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_alert_logs.paginate(page, per_page = pageSize, error_out = False)
    alert_logs = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[alert_log.to_json() for alert_log in alert_logs]
                    })

