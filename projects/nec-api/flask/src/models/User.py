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
        updatedat: 更新时间
        createdat: 创建时间
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(256))
    permission = db.Column(db.JSON)
    updatedat = db.Column(db.DateTime)
    createdat = db.Column(db.DateTime)

    def to_json(self):
        """返回请求json数据

        Returns:
        """
        return{
            'id': self.id,
            'uid': self.uid,
            'permission': self.permission,
            'updatedat': self.updatedat,
            'createdat': self.createdat,
        }

    def __repr__(self):
        return '<User %r>' % self.id
