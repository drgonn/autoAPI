from datetime import datetime  #记录时间
from app import db
from app.tools import utc_switch,generate_token,certify_token,get_permission
from app.standard import Permission
from datetime import datetime  

class Device(db.Model):
	__tablename__='devices'
	id = db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(16), index=True)
	name = db.Column(db.String(64))
	area = db.Column(db.String(64))
	
	def to_json(self):
		return{
			'id':self.id,
			'symbol': self.symbol,
			'name': self.name,
			'area': self.area,
		}

	def __repr__(self):
		return '<Device %r>' % self.name

class Work(db.Model):
	__tablename__='works'
	id = db.Column(db.Integer, primary_key=True)
	start_time = db.Column(db.DateTime)
	end_time = db.Column(db.DateTime)
	seconds = db.Column(db.Integer)
	type = db.Column(db.Integer)
	device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
	device = db.relationship('Device', backref=db.backref('works', lazy='dynamic'))
	
	def to_json(self):
		return{
			'id':self.id,
			'start_time': utc_switch(self.start_time),
			'end_time': utc_switch(self.end_time),
			'seconds': self.seconds,
			'type': self.type,
			'device_name' : self.device.name,
		}

	def __repr__(self):
		return '<Work %r>' % self.id
