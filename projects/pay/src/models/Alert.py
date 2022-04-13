from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Alert(db.Model):
    """报警规则数据库模型

    

    Attributes:
        id: 主键ID
        name: 名称
        webhook: 推送地址
        emails: 告警邮箱
        flow: 报警触发流量
        all: 是否是用户全部卡片
        enable: 规则开启关闭
        description: 描述
        event: 规则类型分类
        updated_at: 更新时间
        created_at: 创建时间
        user_id: 父表users的ID
        user: 父表users对象
    """
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    webhook = db.Column(db.Text)
    emails = db.Column(db.json)
    flow = db.Column(db.Float)
    all = db.Column(db.Boolean)
    enable = db.Column(db.Boolean)
    description = db.Column(db.Text)
    event = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('alerts', lazy='dynamic'))

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'name': self.name,
            'webhook': self.webhook,
            'emails': self.emails,
            'flow': self.flow,
            'all': self.all,
            'enable': self.enable,
            'description': self.description,
            'event': self.event,
            'updated_at': utc_switch(self.updated_at),
            'created_at': utc_switch(self.created_at),
            'user_name': self.user.name if self.user else None,
            'user_id': self.user.id if self.user else None,
        }

    def __repr__(self):
        return '<Alert %r>' % self.id
