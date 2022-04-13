import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

from app.models.sun import Sun



@api.route('/moon/<int:id>', methods=['GET'])
def get_moon(id):
    """get单个月亮接口

    Params:
        id (int, require): 月亮ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 月亮的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            about (text optional): 简介
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    moon = Moon.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': moon.to_json(),
                    })


@api.route('/moon', methods=['POST'])
def create_moon():
    """post创建单个月亮接口

    Requests:
        name (string, require): 名称
        about (text, require): 简介

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 月亮主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    about = request.json.get('about')
    if about is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：about'})

    moon = Moon(
        name=name,
        about=about,
    )

    db.session.add(moon)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': moon.id,
                    })


@api.route('/moon/<int:id>', methods=['PUT'])
def modify_moon(id):
    """put修改单个月亮接口

    Requests:
        name (string, optional): 名称
        about (text, optional): 简介

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    moon = Moon.query.get_or_404(id)
    name = request.json.get('name')
    about = request.json.get('about')
    moon.name = name or moon.name
    moon.about = about or moon.about
    db.session.add(moon)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/moon', methods=['DELETE'])
def delete_moon():
    """delete删除多个月亮接口

    Params:
        ids (list, require): 需要删除的月亮ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        moon = Moon.query.get(id)
        if moon is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(moon)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/moon/list', methods=['GET'])
def list_moon():
    """get查询月亮列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 月亮的json列表
            id (uint optional): 主键ID
            name (string optional): 名称
            about (text optional): 简介
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_moons = Moon.query
    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_moons = total_moons.order_by(Moon.id.asc())
        elif sorter.get('id') == 'descend':
            total_moons = total_moons.order_by(Moon.id.desc())
        if sorter.get('updated_at') == 'ascend':
            total_moons = total_moons.order_by(Moon.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_moons = total_moons.order_by(Moon.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_moons = total_moons.order_by(Moon.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_moons = total_moons.order_by(Moon.created_at.desc())
        pass
    totalcount = total_moons.with_entities(func.count(Moon.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_moons.paginate(page, per_page = pageSize, error_out = False)
    moons = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[moon.to_json() for moon in moons]
                    })

