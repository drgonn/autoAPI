from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Capimg(db.Model):
    """抓拍图片数据库模型

    抓拍的图片记录

    Attributes:
        id: 主键ID
        hikv_url: 图片地址
        created_at: 创建时间
        hikv_id: 父表hikvs的ID
        hikv: 父表hikvs对象
    """
    __tablename__ = 'capimgs'
    id = db.Column(db.Integer, primary_key=True)
    hikv_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hikv_id = db.Column(db.Integer, db.ForeignKey('hikvs.id'))
    hikv = db.relationship('Hikv', backref=db.backref('capimgs', lazy='dynamic'))

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'hikv_url': self.hikv_url,
            'created_at': utc_switch(self.created_at),
        }

    def __repr__(self):
        return '<Capimg %r>' % self.id
