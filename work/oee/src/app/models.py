from flask import request, jsonify, current_app, g
from app import db
from datetime import datetime
from app.tools import utc_switch

class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.String(64), unique=True, index=True, nullable=False)
	name = db.Column(db.String(64))
	createDate = db.Column(db.DateTime, default=datetime.utcnow)
	
	def to_json(self):
		return{
			'id':self.id,
			'uid': self.uid,
			'name': self.name,
			'createDate': utc_switch(self.createDate),
		}

	def __repr__(self):
		return '<User %r>' % self.name

class Device(db.Model):
	__tablename__='devices'
	id = db.Column(db.Integer, primary_key=True)
	sn = db.Column(db.String(16), index=True)
	name = db.Column(db.String(64))
	type = db.Column(db.String(64))
	
	def to_json(self):
		return{
			'id':self.id,
			'sn': self.sn,
			'name': self.name,
			'type': self.type,
		}

	def __repr__(self):
		return '<Device %r>' % self.name

class Worktime(db.Model):
	__tablename__='worktimes'
	id = db.Column(db.Integer, primary_key=True)
	start_time = db.Column(db.DateTime)
	end_time = db.Column(db.DateTime)
	seconds = db.Column(db.Integer)
	type = db.Column(db.Integer)
	amount = db.Column(db.Integer)
	good = db.Column(db.Integer)
	glue = db.Column(db.Float)
	device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
	device = db.relationship('Device', backref=db.backref('worktimes', lazy='dynamic'))
	
	def to_json(self):
		return{
			'id':self.id,
			'start_time': utc_switch(self.start_time),
			'end_time': utc_switch(self.end_time),
			'seconds': self.seconds,
			'type': self.type,
			'amount': self.amount,
			'good': self.good,
			'glue': self.glue,
			'device_name' : self.device.name,
		}

	def __repr__(self):
		return '<Worktime %r>' % self.id

class Valve(db.Model):
	__tablename__='valves'
	id = db.Column(db.Integer, primary_key=True)
	sn = db.Column(db.String(16), index=True)
	name = db.Column(db.String(64))
	type = db.Column(db.String(64))
	device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
	device = db.relationship('Device', backref=db.backref('valves', lazy='dynamic'))
	
	def to_json(self):
		return{
			'id':self.id,
			'sn': self.sn,
			'name': self.name,
			'type': self.type,
			'device_name' : self.device.name,
		}

	def __repr__(self):
		return '<Valve %r>' % self.id

class Role(db.Model):
	__tablename__='roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	permissions = db.Column(db.Integer)
	
	def to_json(self):
		return{
			'id':self.id,
			'name': self.name,
			'permissions': self.permissions,
		}

	def __repr__(self):
		return '<Role %r>' % self.name

class Usercopy(db.Model):
	__tablename__='usercopys'
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.String(64), unique=True, index=True, nullable=False)
	username = db.Column(db.String(64))
	phone = db.Column(db.String(64))
	email = db.Column(db.String(64))
	emailbind = db.Column(db.Boolean)
	company = db.Column(db.String(64))
	address = db.Column(db.String(64))
	url = db.Column(db.String(128))
	nickname = db.Column(db.String(64))
	headimgurl = db.Column(db.String(256))
	createDate = db.Column(db.DateTime, default=datetime.utcnow)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	role = db.relationship('Role', backref=db.backref('usercopys', lazy='dynamic'))
	
	def to_json(self):
		return{
			'id':self.id,
			'uid': self.uid,
			'username': self.username,
			'phone': self.phone,
			'email': self.email,
			'emailbind': self.emailbind,
			'company': self.company,
			'address': self.address,
			'url': self.url,
			'nickname': self.nickname,
			'headimgurl': self.headimgurl,
			'createDate': utc_switch(self.createDate),
			'role_name' : self.role.name,
		}

	def __repr__(self):
		return '<Usercopy %r>' % self.name

class Userlog(db.Model):
	__tablename__='userlogs'
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(64))
	user_agent = db.Column(db.String(1024))
	msg = db.Column(db.Text)
	time = db.Column(db.DateTime, default=datetime.utcnow)
	usercopy_id = db.Column(db.Integer, db.ForeignKey('usercopys.id'))
	usercopy = db.relationship('Usercopy', backref=db.backref('userlogs', lazy='dynamic'))
	
	def to_json(self):
		return{
			'id':self.id,
			'ip': self.ip,
			'user_agent': self.user_agent,
			'msg': self.msg,
			'time': utc_switch(self.time),
			'usercopy_name' : self.usercopy.name,
		}

	def __repr__(self):
		return '<Userlog %r>' % self.name
