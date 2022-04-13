import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/config/<int:id>', methods=['GET'])
def get_config(id):
    """get单个密码配置接口

    Params:
        id (int, require): 密码配置ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 密码配置的详细参数
            id (uint optional): 主键ID
            length (uint optional): 主键ID
            pure_number (bool optional): 摄像头名称
            case_sensitive (bool optional): 摄像头账号的appKey
            special_characters (bool optional): 摄像头账号的appSecret
            auto_expire (uint optional): 摄像头账号的序列号
    """
    config = Config.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': config.to_json(),
                    })


@api.route('/config', methods=['POST'])
def create_config():
    """post创建单个密码配置接口

    Requests:
        pure_number (bool, require): 摄像头名称
        case_sensitive (bool, require): 摄像头账号的appKey
        special_characters (bool, require): 摄像头账号的appSecret
        auto_expire (uint, require): 摄像头账号的序列号

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 密码配置主键ID
    """
    print(request.json)
    pure_number = request.json.get('pure_number')
    if pure_number is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：pure_number'})
    case_sensitive = request.json.get('case_sensitive')
    if case_sensitive is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：case_sensitive'})
    special_characters = request.json.get('special_characters')
    if special_characters is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：special_characters'})
    auto_expire = request.json.get('auto_expire')
    if auto_expire is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：auto_expire'})

    config = Config(
        pure_number=pure_number,
        case_sensitive=case_sensitive,
        special_characters=special_characters,
        auto_expire=auto_expire,
    )

    db.session.add(config)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': config.id,
                    })


@api.route('/config/<int:id>', methods=['PUT'])
def modify_config(id):
    """put修改单个密码配置接口

    Requests:
        pure_number (bool, optional): 摄像头名称
        case_sensitive (bool, optional): 摄像头账号的appKey
        special_characters (bool, optional): 摄像头账号的appSecret
        auto_expire (uint, optional): 摄像头账号的序列号

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    config = Config.query.get_or_404(id)
    pure_number = request.json.get('pure_number')
    case_sensitive = request.json.get('case_sensitive')
    special_characters = request.json.get('special_characters')
    auto_expire = request.json.get('auto_expire')
    config.pure_number = pure_number or config.pure_number
    config.case_sensitive = case_sensitive or config.case_sensitive
    config.special_characters = special_characters or config.special_characters
    config.auto_expire = auto_expire or config.auto_expire
    db.session.add(config)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/config', methods=['DELETE'])
def delete_config():
    """delete删除多个密码配置接口

    Params:
        ids (list, require): 需要删除的密码配置ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        config = Config.query.get(id)
        if config is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(config)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/config/list', methods=['GET'])
def list_config():
    """get查询密码配置列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 密码配置的json列表
            id (uint optional): 主键ID
            length (uint optional): 主键ID
            pure_number (bool optional): 摄像头名称
            case_sensitive (bool optional): 摄像头账号的appKey
            special_characters (bool optional): 摄像头账号的appSecret
            auto_expire (uint optional): 摄像头账号的序列号
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_configs = Config.query
    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_configs = total_configs.order_by(Config.id.asc())
        elif sorter.get('id') == 'descend':
            total_configs = total_configs.order_by(Config.id.desc())
        if sorter.get('length') == 'ascend':
            total_configs = total_configs.order_by(Config.length.asc())
        elif sorter.get('length') == 'descend':
            total_configs = total_configs.order_by(Config.length.desc())
        pass
    totalcount = total_configs.with_entities(func.count(Config.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_configs.paginate(page, per_page = pageSize, error_out = False)
    configs = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[config.to_json() for config in configs]
                    })

