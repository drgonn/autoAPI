import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

from app.models.moon import Moon



@api.route('/star/<int:id>', methods=['GET'])
def get_star(id):
    """get单个星星接口

    Params:
        id (int, require): 星星ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 星星的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            about (text optional): 简介
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    star = Star.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': star.to_json(),
                    })


@api.route('/star', methods=['POST'])
def create_star():
    """post创建单个星星接口

    Requests:
        name (string, require): 名称
        about (text, require): 简介

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 星星主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    about = request.json.get('about')
    if about is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：about'})

    star = Star(
        name=name,
        about=about,
    )

    db.session.add(star)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': star.id,
                    })


@api.route('/star/<int:id>', methods=['PUT'])
def modify_star(id):
    """put修改单个星星接口

    Requests:
        name (string, optional): 名称
        about (text, optional): 简介

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    star = Star.query.get_or_404(id)
    name = request.json.get('name')
    about = request.json.get('about')
    star.name = name or star.name
    star.about = about or star.about
    db.session.add(star)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/star', methods=['DELETE'])
def delete_star():
    """delete删除多个星星接口

    Params:
        ids (list, require): 需要删除的星星ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        star = Star.query.get(id)
        if star is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(star)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/star/list', methods=['GET'])
def list_star():
    """get查询星星列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 星星的json列表
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
    total_stars = Star.query
    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_stars = total_stars.order_by(Star.id.asc())
        elif sorter.get('id') == 'descend':
            total_stars = total_stars.order_by(Star.id.desc())
        if sorter.get('updated_at') == 'ascend':
            total_stars = total_stars.order_by(Star.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_stars = total_stars.order_by(Star.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_stars = total_stars.order_by(Star.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_stars = total_stars.order_by(Star.created_at.desc())
        pass
    totalcount = total_stars.with_entities(func.count(Star.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_stars.paginate(page, per_page = pageSize, error_out = False)
    stars = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[star.to_json() for star in stars]
                    })

