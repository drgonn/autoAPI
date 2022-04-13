from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Star(db.Model):
    """星星数据库模型

    

    Attributes:
        id: 主键ID
        name: 名称
        about: 简介
        updated_at: 更新时间
        created_at: 创建时间
        moon_id: 父表moons的ID
        moon: 父表moons对象
    """
    __tablename__ = 'stars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    moon_id = db.Column(db.Integer, db.ForeignKey('moons.id'))
    moon = db.relationship('Moon', backref=db.backref('stars', lazy='dynamic'))

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
            'moon_name': self.moon.name if self.moon else None,
            'moon_id': self.moon.id if self.moon else None,
        }

    def __repr__(self):
        return '<Star %r>' % self.id
