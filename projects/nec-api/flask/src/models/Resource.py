from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class Resource(db.Model):
    """资源数据库模型

    

    Attributes:
        id: 主键ID
        name: 名称
        description: 描述
        action: 对应的权限
        updatedat: 更新时间
        createdat: 创建时间
    """
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    action = db.Column(db.JSON)
    updatedat = db.Column(db.DateTime)
    createdat = db.Column(db.DateTime)

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'action': self.action,
            'updatedat': self.updatedat,
            'createdat': self.createdat,
        }

    def __repr__(self):
        return '<Resource %r>' % self.id
