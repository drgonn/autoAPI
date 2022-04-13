import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

from app.models.user import User
from app.models.bridge import Bridge
from app.models.component import Component



@api.route('/hikv/<int:id>', methods=['GET'])
def get_hikv(id):
    """get单个摄像头接口

    Params:
        id (int, require): 摄像头ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 摄像头的详细参数
            id (uint optional): 主键ID
            name (string optional): 摄像头名称
            app_key (string optional): 摄像头账号的appKey
            app_secret (string optional): 摄像头账号的appSecret
            hikv_serial (string optional): 摄像头账号的序列号
            validate_code (string optional): 摄像头账号的验证码
            cap_minute (uint optional): 摄像头定时间隔拍照时间
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    hikv = Hikv.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': hikv.to_json(),
                    })


@api.route('/hikv', methods=['POST'])
def create_hikv():
    """post创建单个摄像头接口

    Requests:
        bridge_id (int, optional): 桥梁id主键ID
        component_id (int, optional): 部位id主键ID
        name (string, require): 摄像头名称
        app_key (string, require): 摄像头账号的appKey
        app_secret (string, require): 摄像头账号的appSecret
        hikv_serial (string, require): 摄像头账号的序列号
        validate_code (string, require): 摄像头账号的验证码
        cap_minute (uint, optional): 摄像头定时间隔拍照时间

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 摄像头主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    app_key = request.json.get('app_key')
    if app_key is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：app_key'})
    app_secret = request.json.get('app_secret')
    if app_secret is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：app_secret'})
    hikv_serial = request.json.get('hikv_serial')
    if hikv_serial is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：hikv_serial'})
    validate_code = request.json.get('validate_code')
    if validate_code is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：validate_code'})
    cap_minute = request.json.get('cap_minute')

    bridge_id = request.json.get('bridge_id')

    component_id = request.json.get('component_id')

    hikv = Hikv(
        name=name,
        app_key=app_key,
        app_secret=app_secret,
        hikv_serial=hikv_serial,
        validate_code=validate_code,
        cap_minute=cap_minute,
        user=g.current_user,
        bridge_id=bridge.id,
        component_id=component.id,
    )

    db.session.add(hikv)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': hikv.id,
                    })


@api.route('/hikv/<int:id>', methods=['PUT'])
def modify_hikv(id):
    """put修改单个摄像头接口

    Requests:
        name (string, optional): 摄像头名称
        app_key (string, optional): 摄像头账号的appKey
        app_secret (string, optional): 摄像头账号的appSecret
        hikv_serial (string, optional): 摄像头账号的序列号
        validate_code (string, optional): 摄像头账号的验证码
        cap_minute (uint, optional): 摄像头定时间隔拍照时间

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    hikv = Hikv.query.get_or_404(id)
    name = request.json.get('name')
    app_key = request.json.get('app_key')
    app_secret = request.json.get('app_secret')
    hikv_serial = request.json.get('hikv_serial')
    validate_code = request.json.get('validate_code')
    cap_minute = request.json.get('cap_minute')
    bridge_id = request.json.get('bridge_id')
    bridge = Bridge.query.filter_by(id=bridge_id).first()
    if bridge is None:
        return jsonify({'success':False,'error_code':-1,'errmsg':'bridge_id不存在'})    
    component_id = request.json.get('component_id')
    component = Component.query.filter_by(id=component_id).first()
    if component is None:
        return jsonify({'success':False,'error_code':-1,'errmsg':'component_id不存在'})    
    hikv.name = name or hikv.name
    hikv.app_key = app_key or hikv.app_key
    hikv.app_secret = app_secret or hikv.app_secret
    hikv.hikv_serial = hikv_serial or hikv.hikv_serial
    hikv.validate_code = validate_code or hikv.validate_code
    hikv.cap_minute = cap_minute or hikv.cap_minute
    hikv.bridge_id = bridge.id
    hikv.component_id = component.id
    db.session.add(hikv)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/hikv', methods=['DELETE'])
def delete_hikv():
    """delete删除多个摄像头接口

    Params:
        ids (list, require): 需要删除的摄像头ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        hikv = Hikv.query.get(id)
        if hikv is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(hikv)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/hikv/list', methods=['GET'])
def list_hikv():
    """get查询摄像头列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        bridge_id (int optional): 桥梁id主键ID
        component_id (int optional): 部位id主键ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 摄像头的json列表
            id (uint optional): 主键ID
            name (string optional): 摄像头名称
            app_key (string optional): 摄像头账号的appKey
            app_secret (string optional): 摄像头账号的appSecret
            hikv_serial (string optional): 摄像头账号的序列号
            validate_code (string optional): 摄像头账号的验证码
            cap_minute (uint optional): 摄像头定时间隔拍照时间
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_hikvs = Hikv.query

    bridge_id = request.args.get('bridge_id')
    if bridge_id is not None:
        bridge = Bridge.query.filter_by(id=bridge_id).first()
        if bridge is None:
            return jsonify({'success':False,'error_code':-1,'errmsg':'bridge_id不存在'})
        else:
            total_hikvs = total_hikvs.filter_by(bridge_id=bridge.id)

    component_id = request.args.get('component_id')
    if component_id is not None:
        component = Component.query.filter_by(id=component_id).first()
        if component is None:
            return jsonify({'success':False,'error_code':-1,'errmsg':'component_id不存在'})
        else:
            total_hikvs = total_hikvs.filter_by(component_id=component.id)
    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_hikvs = total_hikvs.order_by(Hikv.id.asc())
        elif sorter.get('id') == 'descend':
            total_hikvs = total_hikvs.order_by(Hikv.id.desc())
        if sorter.get('updated_at') == 'ascend':
            total_hikvs = total_hikvs.order_by(Hikv.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_hikvs = total_hikvs.order_by(Hikv.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_hikvs = total_hikvs.order_by(Hikv.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_hikvs = total_hikvs.order_by(Hikv.created_at.desc())
        pass
    totalcount = total_hikvs.with_entities(func.count(Hikv.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_hikvs.paginate(page, per_page = pageSize, error_out = False)
    hikvs = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[hikv.to_json() for hikv in hikvs]
                    })

