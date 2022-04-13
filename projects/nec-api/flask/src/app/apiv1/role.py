import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/role/<int:id>', methods=['GET'])
def get_role(id):
    """get单个角色接口

    Params:
        id (int, require): 角色ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 角色的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            description (text optional): 描述
            permission (json optional): 权限
            updatedat (datetime optional): 更新时间
            createdat (datetime optional): 创建时间
    """
    role = Role.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': role.to_json(),
                    })


@api.route('/role', methods=['POST'])
def create_role():
    """post创建单个角色接口

    Requests:
        name (string, require): 名称
        description (text, optional): 描述
        permission (json, optional): 权限

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 角色主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    description = request.json.get('description')
    permission = request.json.get('permission')

    role = Role(
        name=name,
        description=description,
        permission=permission,
    )

    db.session.add(role)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': role.id,
                    })


@api.route('/role/<int:id>', methods=['PUT'])
def modify_role(id):
    """put修改单个角色接口

    Requests:
        name (string, optional): 名称
        description (text, optional): 描述
        permission (json, optional): 权限

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    role = Role.query.get_or_404(id)
    name = request.json.get('name')
    description = request.json.get('description')
    permission = request.json.get('permission')
    role.name = name or role.name
    role.description = description or role.description
    role.permission = permission or role.permission
    db.session.add(role)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/role', methods=['DELETE'])
def delete_role():
    """delete删除多个角色接口

    Params:
        ids (list, require): 需要删除的角色ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        role = Role.query.get(id)
        if role is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(role)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/role/list', methods=['GET'])
def list_role():
    """get查询角色列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        name (string optional): 名称，支持模糊匹配,支持排序

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 角色的json列表
            id (uint optional): 主键ID
            name (string optional): 名称
            description (text optional): 描述
            permission (json optional): 权限
            updatedat (datetime optional): 更新时间
            createdat (datetime optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_roles = Role.query
    name = request.args.get('name')
    if name is not None:
        total_roles = total_roles.filter(Role.name.ilike(f'%{name}%'))

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_roles = total_roles.order_by(Role.id.asc())
        elif sorter.get('id') == 'descend':
            total_roles = total_roles.order_by(Role.id.desc())
        if sorter.get('name') == 'ascend':
            total_roles = total_roles.order_by(Role.name.asc())
        elif sorter.get('name') == 'descend':
            total_roles = total_roles.order_by(Role.name.desc())
        if sorter.get('updatedat') == 'ascend':
            total_roles = total_roles.order_by(Role.updatedat.asc())
        elif sorter.get('updatedat') == 'descend':
            total_roles = total_roles.order_by(Role.updatedat.desc())
        if sorter.get('createdat') == 'ascend':
            total_roles = total_roles.order_by(Role.createdat.asc())
        elif sorter.get('createdat') == 'descend':
            total_roles = total_roles.order_by(Role.createdat.desc())
        pass
    totalcount = total_roles.with_entities(func.count(Role.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_roles.paginate(page, per_page = pageSize, error_out = False)
    roles = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[role.to_json() for role in roles]
                    })

