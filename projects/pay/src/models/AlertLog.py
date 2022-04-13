from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class AlertLog(db.Model):
    """告警日志数据库模型

    

    Attributes:
        id: 主键ID
        iccid: 名称
        status: 状态
        updated_at: 更新时间
        created_at: 创建时间
        alert_id: 父表alerts的ID
        alert: 父表alerts对象
    """
    __tablename__ = 'alert_logs'
    id = db.Column(db.Integer, primary_key=True)
    iccid = db.Column(db.String(128))
    status = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'))
    alert = db.relationship('Alert', backref=db.backref('alert_logs', lazy='dynamic'))

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'iccid': self.iccid,
            'status': self.status,
            'updated_at': utc_switch(self.updated_at),
            'created_at': utc_switch(self.created_at),
            'alert_name': self.alert.name if self.alert else None,
            'alert_id': self.alert.id if self.alert else None,
        }

    def __repr__(self):
        return '<AlertLog %r>' % self.id
