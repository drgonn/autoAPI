from datetime import datetime  #记录时间
from app import db
from app.tools import utc_switch,generate_token,certify_token,get_permission
from app.standard import Permission
from datetime import datetime  

class Stock(db.Model):
	__tablename__='stocks'
	id = db.Column(db.Integer, primary_key=True)
	ts_code = db.Column(db.String(16))
	symbol = db.Column(db.String(16), unique=True, index=True)
	name = db.Column(db.String(64))
	area = db.Column(db.String(64))
	industry = db.Column(db.String(64))
	fullname = db.Column(db.String(64))
	enname = db.Column(db.String(64))
	market = db.Column(db.String(64))
	exchange = db.Column(db.String(64))
	curr_type = db.Column(db.String(64))
	list_status = db.Column(db.String(64))
	list_date = db.Column(db.String(64))
	delist_date = db.Column(db.String(64))
	is_hs = db.Column(db.String(8))
	price = db.Column(db.Float)
	
	def to_json(self):
		return{
			'id':self.id,
			'ts_code':self.ts_code,
			'symbol':self.symbol,
			'name':self.name,
			'area':self.area,
			'industry':self.industry,
			'fullname':self.fullname,
			'enname':self.enname,
			'market':self.market,
			'exchange':self.exchange,
			'curr_type':self.curr_type,
			'list_status':self.list_status,
			'list_date':self.list_date,
			'delist_date':self.delist_date,
			'is_hs':self.is_hs,
			'price':self.price,
		}

	def __repr__(self):
		return '<Stock %r>' % self.name
