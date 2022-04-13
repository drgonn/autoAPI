import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    """get单个用户接口

    Params:
        id (int, require): 用户ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 用户的详细参数
            id (uint optional): 主键ID
            uid (string optional): UID
            permission (json optional): 权限
            updated_at (datetime optional): 更新时间
            created_at (datetime optional): 创建时间
    """
    user = User.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': user.to_json(),
                    })


@api.route('/user', methods=['POST'])
def create_user():
    """post创建单个用户接口

    Requests:
        uid (string, optional): UID
        permission (json, optional): 权限

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 用户主键ID
    """
    print(request.json)
    uid = request.json.get('uid')
    permission = request.json.get('permission')

    user = User(
        uid=uid,
        permission=permission,
    )

    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': user.id,
                    })


@api.route('/user/<int:id>', methods=['PUT'])
def modify_user(id):
    """put修改单个用户接口

    Requests:
        uid (string, optional): UID
        permission (json, optional): 权限

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    user = User.query.get_or_404(id)
    uid = request.json.get('uid')
    permission = request.json.get('permission')
    user.uid = uid or user.uid
    user.permission = permission or user.permission
    db.session.add(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/user', methods=['DELETE'])
def delete_user():
    """delete删除多个用户接口

    Params:
        ids (list, require): 需要删除的用户ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        user = User.query.get(id)
        if user is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/user/list', methods=['GET'])
def list_user():
    """get查询用户列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        uid (string optional): UID,支持精确匹配

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 用户的json列表
            id (uint optional): 主键ID
            uid (string optional): UID
            permission (json optional): 权限
            updated_at (datetime optional): 更新时间
            created_at (datetime optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_users = User.query
    uid = request.args.get('uid')
    if uid is not None:
        total_users = total_users.filter_by(uid=uid)

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_users = total_users.order_by(User.id.asc())
        elif sorter.get('id') == 'descend':
            total_users = total_users.order_by(User.id.desc())
        if sorter.get('updated_at') == 'ascend':
            total_users = total_users.order_by(User.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_users = total_users.order_by(User.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_users = total_users.order_by(User.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_users = total_users.order_by(User.created_at.desc())
        pass
    totalcount = total_users.with_entities(func.count(User.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_users.paginate(page, per_page = pageSize, error_out = False)
    users = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[user.to_json() for user in users]
                    })

