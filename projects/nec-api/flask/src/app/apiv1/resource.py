import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/resource/<int:id>', methods=['GET'])
def get_resource(id):
    """get单个资源接口

    Params:
        id (int, require): 资源ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 资源的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            description (text optional): 描述
            action (json optional): 对应的权限
            updatedat (datetime optional): 更新时间
            createdat (datetime optional): 创建时间
    """
    resource = Resource.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': resource.to_json(),
                    })


@api.route('/resource', methods=['POST'])
def create_resource():
    """post创建单个资源接口

    Requests:
        name (string, require): 名称
        description (text, optional): 描述
        action (json, optional): 对应的权限

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 资源主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    description = request.json.get('description')
    action = request.json.get('action')

    resource = Resource(
        name=name,
        description=description,
        action=action,
    )

    db.session.add(resource)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': resource.id,
                    })


@api.route('/resource/<int:id>', methods=['PUT'])
def modify_resource(id):
    """put修改单个资源接口

    Requests:
        description (text, optional): 描述
        action (json, optional): 对应的权限

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    resource = Resource.query.get_or_404(id)
    description = request.json.get('description')
    action = request.json.get('action')
    resource.description = description or resource.description
    resource.action = action or resource.action
    db.session.add(resource)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/resource', methods=['DELETE'])
def delete_resource():
    """delete删除多个资源接口

    Params:
        ids (list, require): 需要删除的资源ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        resource = Resource.query.get(id)
        if resource is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(resource)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/resource/list', methods=['GET'])
def list_resource():
    """get查询资源列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        name (string optional): 名称，支持模糊匹配,支持排序

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 资源的json列表
            id (uint optional): 主键ID
            name (string optional): 名称
            description (text optional): 描述
            action (json optional): 对应的权限
            updatedat (datetime optional): 更新时间
            createdat (datetime optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_resources = Resource.query
    name = request.args.get('name')
    if name is not None:
        total_resources = total_resources.filter(Resource.name.ilike(f'%{name}%'))

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_resources = total_resources.order_by(Resource.id.asc())
        elif sorter.get('id') == 'descend':
            total_resources = total_resources.order_by(Resource.id.desc())
        if sorter.get('name') == 'ascend':
            total_resources = total_resources.order_by(Resource.name.asc())
        elif sorter.get('name') == 'descend':
            total_resources = total_resources.order_by(Resource.name.desc())
        if sorter.get('updatedat') == 'ascend':
            total_resources = total_resources.order_by(Resource.updatedat.asc())
        elif sorter.get('updatedat') == 'descend':
            total_resources = total_resources.order_by(Resource.updatedat.desc())
        if sorter.get('createdat') == 'ascend':
            total_resources = total_resources.order_by(Resource.createdat.asc())
        elif sorter.get('createdat') == 'descend':
            total_resources = total_resources.order_by(Resource.createdat.desc())
        pass
    totalcount = total_resources.with_entities(func.count(Resource.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_resources.paginate(page, per_page = pageSize, error_out = False)
    resources = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[resource.to_json() for resource in resources]
                    })

