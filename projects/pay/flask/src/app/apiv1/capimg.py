import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

from app.models.hikv import Hikv



@api.route('/inspect/capimg/<int:id>', methods=['GET'])
def get_capimg(id):
    """get单个抓拍图片接口

    Params:
        id (int, require): 抓拍图片ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 抓拍图片的详细参数
            id (uint optional): 主键ID
            hikv_url (string optional): 图片地址
            created_at (time optional): 创建时间
    """
    capimg = Capimg.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': capimg.to_json(),
                    })


@api.route('/inspect/capimg', methods=['POST'])
def create_capimg():
    """post创建单个抓拍图片接口

    Requests:

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 抓拍图片主键ID
    """
    print(request.json)

    capimg = Capimg(
    )

    db.session.add(capimg)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': capimg.id,
                    })


@api.route('/inspect/capimg/<int:id>', methods=['PUT'])
def modify_capimg(id):
    """put修改单个抓拍图片接口

    Requests:
        hikv_url (string, optional): 图片地址

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    capimg = Capimg.query.get_or_404(id)
    hikv_url = request.json.get('hikv_url')
    capimg.hikv_url = hikv_url or capimg.hikv_url
    db.session.add(capimg)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/inspect/capimg', methods=['DELETE'])
def delete_capimg():
    """delete删除多个抓拍图片接口

    Params:
        ids (list, require): 需要删除的抓拍图片ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        capimg = Capimg.query.get(id)
        if capimg is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(capimg)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/inspect/capimg/list', methods=['GET'])
def list_capimg():
    """get查询抓拍图片列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        hikv_id (int optional): card id主键ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 抓拍图片的json列表
            id (uint optional): 主键ID
            hikv_url (string optional): 图片地址
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_capimgs = Capimg.query

    hikv_id = request.args.get('hikv_id')
    if hikv_id is not None:
        hikv = Hikv.query.filter_by(id=hikv_id).first()
        if hikv is None:
            return jsonify({'success':False,'error_code':-1,'errmsg':'hikv_id不存在'})
        else:
            total_capimgs = total_capimgs.filter_by(hikv_id=hikv.id)
    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_capimgs = total_capimgs.order_by(Capimg.id.asc())
        elif sorter.get('id') == 'descend':
            total_capimgs = total_capimgs.order_by(Capimg.id.desc())
        if sorter.get('created_at') == 'ascend':
            total_capimgs = total_capimgs.order_by(Capimg.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_capimgs = total_capimgs.order_by(Capimg.created_at.desc())
        pass
    totalcount = total_capimgs.with_entities(func.count(Capimg.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_capimgs.paginate(page, per_page = pageSize, error_out = False)
    capimgs = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[capimg.to_json() for capimg in capimgs]
                    })

