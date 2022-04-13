from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Moon(db.Model):
    """月亮数据库模型

    

    Attributes:
        id: 主键ID
        name: 名称
        about: 简介
        updated_at: 更新时间
        created_at: 创建时间
        sun_id: 父表suns的ID
        sun: 父表suns对象
    """
    __tablename__ = 'moons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sun_id = db.Column(db.Integer, db.ForeignKey('suns.id'))
    sun = db.relationship('Sun', backref=db.backref('moons', lazy='dynamic'))

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'updated_at': utc_switch(self.updated_at),
            'created_at': utc_switch(self.created_at),
            'sun_name': self.sun.name if self.sun else None,
            'sun_id': self.sun.id if self.sun else None,
        }

    def __repr__(self):
        return '<Moon %r>' % self.id
