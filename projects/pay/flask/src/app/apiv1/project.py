import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func




@api.route('/project/<int:id>', methods=['GET'])
def get_project(id):
    """get单个项目接口

    Params:
        id (int, require): 项目ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 项目的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            puid (string optional): PID
            ouid (string optional): 租户UID
            describe (text optional): 描述
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    project = Project.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': project.to_json(),
                    })


@api.route('/project', methods=['POST'])
def create_project():
    """post创建单个项目接口

    Requests:
        name (string, require): 名称
        ouid (string, optional): 租户UID
        describe (text, optional): 描述

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 项目主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    ouid = request.json.get('ouid')
    describe = request.json.get('describe')

    project = Project(
        name=name,
        ouid=ouid,
        describe=describe,
    )

    db.session.add(project)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': project.id,
                    })


@api.route('/project/<int:id>', methods=['PUT'])
def modify_project(id):
    """put修改单个项目接口

    Requests:
        name (string, optional): 名称
        ouid (string, optional): 租户UID
        describe (text, optional): 描述

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    project = Project.query.get_or_404(id)
    name = request.json.get('name')
    ouid = request.json.get('ouid')
    describe = request.json.get('describe')
    project.name = name or project.name
    project.ouid = ouid or project.ouid
    project.describe = describe or project.describe
    db.session.add(project)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/project', methods=['DELETE'])
def delete_project():
    """delete删除多个项目接口

    Params:
        ids (list, require): 需要删除的项目ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        project = Project.query.get(id)
        if project is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(project)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/project/list', methods=['GET'])
def list_project():
    """get查询项目列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        name (string optional): 名称，支持模糊匹配,支持排序
        puid (string optional): PID,支持精确匹配
        ouid (string optional): 租户UID,支持精确匹配
        describe (text optional): 描述，支持模糊匹配

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 项目的json列表
            id (uint optional): 主键ID
            name (string optional): 名称
            puid (string optional): PID
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
    total_projects = Project.query
    name = request.args.get('name')
    if name is not None:
        total_projects = total_projects.filter(Project.name.ilike(f'%{name}%'))

    puid = request.args.get('puid')
    if puid is not None:
        total_projects = total_projects.filter_by(puid=puid)

    ouid = request.args.get('ouid')
    if ouid is not None:
        total_projects = total_projects.filter_by(ouid=ouid)

    describe = request.args.get('describe')
    if describe is not None:
        total_projects = total_projects.filter(Project.describe.ilike(f'%{describe}%'))

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_projects = total_projects.order_by(Project.id.asc())
        elif sorter.get('id') == 'descend':
            total_projects = total_projects.order_by(Project.id.desc())
        if sorter.get('name') == 'ascend':
            total_projects = total_projects.order_by(Project.name.asc())
        elif sorter.get('name') == 'descend':
            total_projects = total_projects.order_by(Project.name.desc())
        if sorter.get('updated_at') == 'ascend':
            total_projects = total_projects.order_by(Project.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_projects = total_projects.order_by(Project.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_projects = total_projects.order_by(Project.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_projects = total_projects.order_by(Project.created_at.desc())
        pass
    totalcount = total_projects.with_entities(func.count(Project.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_projects.paginate(page, per_page = pageSize, error_out = False)
    projects = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[project.to_json() for project in projects]
                    })

