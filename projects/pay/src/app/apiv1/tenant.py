import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/tenant/<int:id>', methods=['GET'])
def get_tenant(id):
    """get单个租户接口

    Params:
        id (int, require): 租户ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 租户的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            ouid (string optional): 租户UID
            describe (text optional): 描述
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    tenant = Tenant.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': tenant.to_json(),
                    })


@api.route('/tenant', methods=['POST'])
def create_tenant():
    """post创建单个租户接口

    Requests:
        name (string, require): 名称
        describe (text, optional): 描述

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 租户主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    describe = request.json.get('describe')

    tenant = Tenant(
        name=name,
        describe=describe,
    )

    db.session.add(tenant)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': tenant.id,
                    })


@api.route('/tenant/<int:id>', methods=['PUT'])
def modify_tenant(id):
    """put修改单个租户接口

    Requests:
        name (string, optional): 名称
        describe (text, optional): 描述

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    tenant = Tenant.query.get_or_404(id)
    name = request.json.get('name')
    describe = request.json.get('describe')
    tenant.name = name or tenant.name
    tenant.describe = describe or tenant.describe
    db.session.add(tenant)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/tenant', methods=['DELETE'])
def delete_tenant():
    """delete删除多个租户接口

    Params:
        ids (list, require): 需要删除的租户ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        tenant = Tenant.query.get(id)
        if tenant is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(tenant)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/tenant/list', methods=['GET'])
def list_tenant():
    """get查询租户列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        name (string optional): 名称，支持模糊匹配,支持排序
        ouid (string optional): 租户UID,支持精确匹配
        describe (text optional): 描述，支持模糊匹配

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 租户的json列表
            id (uint optional): 主键ID
            name (string optional): 名称
            ouid (string optional): 租户UID
            describe (text optional): 描述
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_tenants = Tenant.query
    name = request.args.get('name')
    if name is not None:
        total_tenants = total_tenants.filter(Tenant.name.ilike(f'%{name}%'))

    ouid = request.args.get('ouid')
    if ouid is not None:
        total_tenants = total_tenants.filter_by(ouid=ouid)

    describe = request.args.get('describe')
    if describe is not None:
        total_tenants = total_tenants.filter(Tenant.describe.ilike(f'%{describe}%'))

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_tenants = total_tenants.order_by(Tenant.id.asc())
        elif sorter.get('id') == 'descend':
            total_tenants = total_tenants.order_by(Tenant.id.desc())
        if sorter.get('name') == 'ascend':
            total_tenants = total_tenants.order_by(Tenant.name.asc())
        elif sorter.get('name') == 'descend':
            total_tenants = total_tenants.order_by(Tenant.name.desc())
        if sorter.get('updated_at') == 'ascend':
            total_tenants = total_tenants.order_by(Tenant.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_tenants = total_tenants.order_by(Tenant.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_tenants = total_tenants.order_by(Tenant.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_tenants = total_tenants.order_by(Tenant.created_at.desc())
        pass
    totalcount = total_tenants.with_entities(func.count(Tenant.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_tenants.paginate(page, per_page = pageSize, error_out = False)
    tenants = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[tenant.to_json() for tenant in tenants]
                    })

