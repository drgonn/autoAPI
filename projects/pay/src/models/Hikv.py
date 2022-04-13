from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Hikv(db.Model):
    """摄像头数据库模型

    摄像头

    Attributes:
        id: 主键ID
        name: 摄像头名称
        app_key: 摄像头账号的appKey
        app_secret: 摄像头账号的appSecret
        hikv_serial: 摄像头账号的序列号
        validate_code: 摄像头账号的验证码
        cap_minute: 摄像头定时间隔拍照时间
        updated_at: 更新时间
        created_at: 创建时间
        user_id: 父表users的ID
        user: 父表users对象
        bridge_id: 父表bridges的ID
        bridge: 父表bridges对象
        component_id: 父表components的ID
        component: 父表components对象
    """
    __tablename__ = 'hikvs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    app_key = db.Column(db.String(64))
    app_secret = db.Column(db.String(64))
    hikv_serial = db.Column(db.String(64))
    validate_code = db.Column(db.String(64))
    cap_minute = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('hikvs', lazy='dynamic'))
    bridge_id = db.Column(db.Integer, db.ForeignKey('bridges.id'))
    bridge = db.relationship('Bridge', backref=db.backref('hikvs', lazy='dynamic'))
    component_id = db.Column(db.Integer, db.ForeignKey('components.id'))
    component = db.relationship('Component', backref=db.backref('hikvs', lazy='dynamic'))

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'name': self.name,
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'hikv_serial': self.hikv_serial,
            'validate_code': self.validate_code,
            'cap_minute': self.cap_minute,
            'updated_at': utc_switch(self.updated_at),
            'created_at': utc_switch(self.created_at),
            'user_name': self.user.name if self.user else None,
            'user_id': self.user.id if self.user else None,
            'bridge_name': self.bridge.name if self.bridge else None,
            'bridge_id': self.bridge.id if self.bridge else None,
            'component_sn': self.component.sn if self.component else None,
            'component_id': self.component.id if self.component else None,
        }

    def __repr__(self):
        return '<Hikv %r>' % self.id
