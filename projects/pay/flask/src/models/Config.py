from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Config(db.Model):
    """密码配置数据库模型

    摄像头

    Attributes:
        id: 主键ID
        length: 主键ID
        pure_number: 摄像头名称
        case_sensitive: 摄像头账号的appKey
        special_characters: 摄像头账号的appSecret
        auto_expire: 摄像头账号的序列号
    """
    __tablename__ = 'configs'
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Integer)
    pure_number = db.Column(db.Boolean)
    case_sensitive = db.Column(db.Boolean)
    special_characters = db.Column(db.Boolean)
    auto_expire = db.Column(db.Integer)

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'length': self.length,
            'pure_number': self.pure_number,
            'case_sensitive': self.case_sensitive,
            'special_characters': self.special_characters,
            'auto_expire': self.auto_expire,
        }

    def __repr__(self):
        return '<Config %r>' % self.id
