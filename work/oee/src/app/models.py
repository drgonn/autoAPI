from datetime import datetime  #记录时间
from app import db
from app.tools import utc_switch,generate_token,certify_token,get_permission
from app.standard import Permission
from datetime import datetime  

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
