import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

from app.models.user import User



@api.route('/alert/<int:id>', methods=['GET'])
def get_alert(id):
    """get单个报警规则接口

    Params:
        id (int, require): 报警规则ID

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        records (json): 报警规则的详细参数
            id (uint optional): 主键ID
            name (string optional): 名称
            webhook (text optional): 推送地址
            emails (json optional): 告警邮箱
            flow (float optional): 报警触发流量
            all (bool optional): 是否是用户全部卡片, 0是, 1否
            enable (bool optional): 规则开启关闭, 0关闭, 1开启
            description (text optional): 描述, 1可激活, 2已激活, 3已停用
            event (int optional): 规则类型分类, 1状态监控, 2流量值监控, 3流量比例监控
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    alert = Alert.query.get_or_404(id)

    return jsonify({'success': True,
                    'error_code': 0,
                    'records': alert.to_json(),
                    })


@api.route('/alert', methods=['POST'])
def create_alert():
    """post创建单个报警规则接口

    Requests:
        name (string, require): 名称
        webhook (text, optional): 推送地址
        emails (json, optional): 告警邮箱
        flow (float, optional): 报警触发流量
        all (bool, optional): 是否是用户全部卡片, 0是, 1否
        enable (bool, optional): 规则开启关闭, 0关闭, 1开启
        description (text, optional): 描述, 1可激活, 2已激活, 3已停用
        event (int, optional): 规则类型分类, 1状态监控, 2流量值监控, 3流量比例监控

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        id (int): 报警规则主键ID
    """
    print(request.json)
    name = request.json.get('name')
    if name is None:
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：name'})
    webhook = request.json.get('webhook')
    emails = request.json.get('emails')
    flow = request.json.get('flow')
    all = request.json.get('all')
    enable = request.json.get('enable')
    description = request.json.get('description')
    event = request.json.get('event')

    alert = Alert(
        name=name,
        webhook=webhook,
        emails=emails,
        flow=flow,
        all=all,
        enable=enable,
        description=description,
        event=event,
        user=g.current_user,
    )

    db.session.add(alert)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'添加数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'})

    return jsonify({'success': True,
                    'error_code': 0,
                    'id': alert.id,
                    })


@api.route('/alert/<int:id>', methods=['PUT'])
def modify_alert(id):
    """put修改单个报警规则接口

    Requests:
        name (string, optional): 名称
        webhook (text, optional): 推送地址
        emails (json, optional): 告警邮箱
        flow (float, optional): 报警触发流量
        all (bool, optional): 是否是用户全部卡片, 0是, 1否
        enable (bool, optional): 规则开启关闭, 0关闭, 1开启
        description (text, optional): 描述, 1可激活, 2已激活, 3已停用
        event (int, optional): 规则类型分类, 1状态监控, 2流量值监控, 3流量比例监控

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print(request.json)
    alert = Alert.query.get_or_404(id)
    name = request.json.get('name')
    webhook = request.json.get('webhook')
    emails = request.json.get('emails')
    flow = request.json.get('flow')
    all = request.json.get('all')
    enable = request.json.get('enable')
    description = request.json.get('description')
    event = request.json.get('event')
    alert.name = name or alert.name
    alert.webhook = webhook or alert.webhook
    alert.emails = emails or alert.emails
    alert.flow = flow or alert.flow
    alert.all = all or alert.all
    alert.enable = enable or alert.enable
    alert.description = description or alert.description
    alert.event = event or alert.event
    db.session.add(alert)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'修改数据库发生错误,已经回退:{e}')
    return jsonify({'success':True,
                    'error_code':0,
                    })


@api.route('/alert', methods=['DELETE'])
def delete_alert():
    """delete删除多个报警规则接口

    Params:
        ids (list, require): 需要删除的报警规则ID主键列表，当包含关联子表时，会删除失败

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
    """
    print('delete json:',request.json)
    ids = request.json.get('ids')
    for id in ids:
        alert = Alert.query.get(id)
        if alert is None:
            return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {id} 不存在'})
        db.session.delete(alert)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'删除数据库发生错误,已经回退:{e}')
        return jsonify({'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {e} '})

    return jsonify({'success':True,
                'error_code':0,
                })


@api.route('/alert/list', methods=['GET'])
def list_alert():
    """get查询报警规则列表接口

    Args:
        page (int, optional): 指定过滤条件，页数Args:
        pageSize (int, optional): 指定过滤条件，单页最大个数Args:
        name (string optional): 名称，支持模糊匹配,支持排序
        webhook (text optional): 推送地址,支持精确匹配
        emails (json optional): 告警邮箱，支持模糊匹配
        flow (float optional): 报警触发流量，支持模糊匹配
        all (bool optional): 是否是用户全部卡片，支持模糊匹配, 0是, 1否
        enable (bool optional): 规则开启关闭，支持模糊匹配, 0关闭, 1开启
        description (text optional): 描述，支持模糊匹配, 1可激活, 2已激活, 3已停用
        event (int optional): 规则类型分类，支持模糊匹配, 1状态监控, 2流量值监控, 3流量比例监控

    Returns:
        success (bool): 请求成功与否
        error_code (int): 错误代码，无错为0
        data (list): 报警规则的json列表
            id (uint optional): 主键ID
            name (string optional): 名称
            webhook (text optional): 推送地址
            emails (json optional): 告警邮箱
            flow (float optional): 报警触发流量
            all (bool optional): 是否是用户全部卡片, 0是, 1否
            enable (bool optional): 规则开启关闭, 0关闭, 1开启
            description (text optional): 描述, 1可激活, 2已激活, 3已停用
            event (int optional): 规则类型分类, 1状态监控, 2流量值监控, 3流量比例监控
            updated_at (time optional): 更新时间
            created_at (time optional): 创建时间
    """
    print(request.args)
    sorter = request.args.get('sorter')
    page = int(request.args.get('current', 1))
    pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))
    pageSize = 20 if pageSize < 10 else pageSize
    total_alerts = Alert.query
    name = request.args.get('name')
    if name is not None:
        total_alerts = total_alerts.filter(Alert.name.ilike(f'%{name}%'))

    webhook = request.args.get('webhook')
    if webhook is not None:
        total_alerts = total_alerts.filter_by(webhook=webhook)

    emails = request.args.get('emails')
    if emails is not None:
        total_alerts = total_alerts.filter(Alert.emails.ilike(f'%{emails}%'))

    flow = request.args.get('flow')
    if flow is not None:
        total_alerts = total_alerts.filter(Alert.flow.ilike(f'%{flow}%'))

    all = request.args.get('all')
    if all is not None:
        total_alerts = total_alerts.filter(Alert.all.ilike(f'%{all}%'))

    enable = request.args.get('enable')
    if enable is not None:
        total_alerts = total_alerts.filter(Alert.enable.ilike(f'%{enable}%'))

    description = request.args.get('description')
    if description is not None:
        total_alerts = total_alerts.filter(Alert.description.ilike(f'%{description}%'))

    event = request.args.get('event')
    if event is not None:
        total_alerts = total_alerts.filter(Alert.event.ilike(f'%{event}%'))

    if sorter:
        sorter = json.loads(sorter)
        if sorter.get('id') == 'ascend':
            total_alerts = total_alerts.order_by(Alert.id.asc())
        elif sorter.get('id') == 'descend':
            total_alerts = total_alerts.order_by(Alert.id.desc())
        if sorter.get('name') == 'ascend':
            total_alerts = total_alerts.order_by(Alert.name.asc())
        elif sorter.get('name') == 'descend':
            total_alerts = total_alerts.order_by(Alert.name.desc())
        if sorter.get('updated_at') == 'ascend':
            total_alerts = total_alerts.order_by(Alert.updated_at.asc())
        elif sorter.get('updated_at') == 'descend':
            total_alerts = total_alerts.order_by(Alert.updated_at.desc())
        if sorter.get('created_at') == 'ascend':
            total_alerts = total_alerts.order_by(Alert.created_at.asc())
        elif sorter.get('created_at') == 'descend':
            total_alerts = total_alerts.order_by(Alert.created_at.desc())
        pass
    totalcount = total_alerts.with_entities(func.count(Alert.id)).scalar()
    page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page
    pagination = total_alerts.paginate(page, per_page = pageSize, error_out = False)
    alerts = pagination.items

    return jsonify({
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[alert.to_json() for alert in alerts]
                    })

