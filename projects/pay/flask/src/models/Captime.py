from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Captime(db.Model):
    """定时计划数据库模型

    定时任务时间

    Attributes:
        id: 主键ID
        iccid: 卡iccid
        status: 通知返回状态码
        created_at: 创建时间
        hikv_id: 父表hikvs的ID
        hikv: 父表hikvs对象
    """
    __tablename__ = 'captimes'
    id = db.Column(db.Integer, primary_key=True)
    iccid = db.Column(db.String(128))
    status = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hikv_id = db.Column(db.Integer, db.ForeignKey('hikvs.id'))
    hikv = db.relationship('Hikv', backref=db.backref('captimes', lazy='dynamic'))

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'iccid': self.iccid,
            'status': self.status,
            'created_at': utc_switch(self.created_at),
        }

    def __repr__(self):
        return '<Captime %r>' % self.id
