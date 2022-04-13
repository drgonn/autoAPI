from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime,date
from app.tools import utc_switch


class User(db.Model):
    """用户数据库模型

    

    Attributes:
        id: 主键ID
        uid: UID
        permission: 权限
        updated_at: 更新时间
        created_at: 创建时间
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(256))
    permission = db.Column(db.JSON)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'uid': self.uid,
            'permission': self.permission,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
        }

    def __repr__(self):
        return '<User %r>' % self.id
