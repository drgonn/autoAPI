import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/sun/<int:id>', methods=['GET'])
def get_sun(id):
    """get单个太阳接口

    Params:
        id (int, require): 太阳ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 太阳的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            about (text optional): 简介
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    sun = Sun.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': sun.to_json(),
                    })


@api.route('/sun', methods=['POST'])
def create_sun():
    """post创建单个太阳接口

    Requests:
        name (string, require): 名称
        about (text, require): 简介

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 太阳主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    about = request.json.get('about')
    if about is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：about'})

    sun = Sun(
        name=name,
        about=about,
    )

    db.session.add(sun)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': sun.id,
                    })


@api.route('/sun/<int:id>', methods=['PUT'])
def modify_sun(id):
    """put修改单个太阳接口

    Requests:
        name (string, optional): 名称
        about (text, optional): 简介

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    sun = Sun.query.get_or_404(id)
    name = request.json.get('name')
    about = request.json.get('about')
    sun.name = name or sun.name
    sun.about = about or sun.about
    db.session.add(sun)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/sun', methods=['DELETE'])
def delete_sun():
    """delete删除多个太阳接口

    Params:
        ids (list, require): 需要删除的太阳ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        sun = Sun.query.get(id)
        if sun is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(sun)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/sun/list', methods=['GET'])
def list_sun():
    """get查询太阳列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 太阳的json列表
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
    total_suns = Sun.query
    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_suns = total_suns.order_by(Sun.id.asc())
        elif sorter.get('id') == 'descend':
            total_suns = total_suns.order_by(Sun.id.desc())
        if sorter.get('updated_at') == 'ascend':
            total_suns = total_suns.order_by(Sun.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_suns = total_suns.order_by(Sun.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_suns = total_suns.order_by(Sun.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_suns = total_suns.order_by(Sun.created_at.desc())
        pass
    totalcount = total_suns.with_entities(func.count(Sun.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_suns.paginate(page, per_page = pageSize, error_out = False)
    suns = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[sun.to_json() for sun in suns]
                    })

