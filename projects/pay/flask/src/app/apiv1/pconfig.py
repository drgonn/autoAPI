import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/pconfig/<int:id>', methods=['GET'])
def get_pconfig(id):
    """get单个配置接口

    Params:
        id (int, require): 配置ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 配置的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            puid (string optional): PID
            value (text optional): value
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    pconfig = Pconfig.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': pconfig.to_json(),
                    })


@api.route('/pconfig', methods=['POST'])
def create_pconfig():
    """post创建单个配置接口

    Requests:
        name (string, require): 名称
        puid (string, optional): PID
        value (text, optional): value

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 配置主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    puid = request.json.get('puid')
    value = request.json.get('value')

    pconfig = Pconfig(
        name=name,
        puid=puid,
        value=value,
    )

    db.session.add(pconfig)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': pconfig.id,
                    })


@api.route('/pconfig/<int:id>', methods=['PUT'])
def modify_pconfig(id):
    """put修改单个配置接口

    Requests:
        name (string, optional): 名称
        puid (string, optional): PID
        value (text, optional): value

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    pconfig = Pconfig.query.get_or_404(id)
    name = request.json.get('name')
    puid = request.json.get('puid')
    value = request.json.get('value')
    pconfig.name = name or pconfig.name
    pconfig.puid = puid or pconfig.puid
    pconfig.value = value or pconfig.value
    db.session.add(pconfig)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/pconfig', methods=['DELETE'])
def delete_pconfig():
    """delete删除多个配置接口

    Params:
        ids (list, require): 需要删除的配置ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        pconfig = Pconfig.query.get(id)
        if pconfig is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(pconfig)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/pconfig/list', methods=['GET'])
def list_pconfig():
    """get查询配置列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        name (string optional): 名称，支持模糊匹配,支持排序
        puid (string optional): PID,支持精确匹配
        value (text optional): value，支持模糊匹配

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 配置的json列表
            id (uint optional): 主键ID
            name (string optional): 名称
            puid (string optional): PID
            value (text optional): value
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_pconfigs = Pconfig.query
    name = request.args.get('name')
    if name is not None:
        total_pconfigs = total_pconfigs.filter(Pconfig.name.ilike(f'%{name}%'))

    puid = request.args.get('puid')
    if puid is not None:
        total_pconfigs = total_pconfigs.filter_by(puid=puid)

    value = request.args.get('value')
    if value is not None:
        total_pconfigs = total_pconfigs.filter(Pconfig.value.ilike(f'%{value}%'))

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.id.asc())
        elif sorter.get('id') == 'descend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.id.desc())
        if sorter.get('name') == 'ascend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.name.asc())
        elif sorter.get('name') == 'descend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.name.desc())
        if sorter.get('updated_at') == 'ascend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_pconfigs = total_pconfigs.order_by(Pconfig.created_at.desc())
        pass
    totalcount = total_pconfigs.with_entities(func.count(Pconfig.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_pconfigs.paginate(page, per_page = pageSize, error_out = False)
    pconfigs = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[pconfig.to_json() for pconfig in pconfigs]
                    })

