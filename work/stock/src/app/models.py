from datetime import datetime  #记录时间
from app import db
from app.tools import utc_switch,generate_token,certify_token,get_permission
from app.standard import Permission
from datetime import datetime  

StockGroup = db.Table('stockgroups',
	db.Column('stock_id',db.Integer,db.ForeignKey('stocks.id')),
	db.Column('group_id',db.Integer,db.ForeignKey('groups.id')))

class Stock(db.Model):
	__tablename__='stocks'
	id = db.Column(db.Integer, primary_key=True)
	ts_code = db.Column(db.String(16), index=True)
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
	list_date = db.Column(db.Date)
	delist_date = db.Column(db.Date)
	is_hs = db.Column(db.String(8))
	price = db.Column(db.Float)
	circ_mv = db.Column(db.Float)
	pe = db.Column(db.Float)

	groups = db.relationship('Group',
		secondary = StockGroup,
		backref = db.backref('stocks',lazy='dynamic'),
		lazy = 'dynamic')
	
	def to_json(self):
		return{
			'id':self.id,
			'ts_code': self.ts_code,
			'symbol': self.symbol,
			'name': self.name,
			'area': self.area,
			'industry': self.industry,
			'fullname': self.fullname,
			'enname': self.enname,
			'market': self.market,
			'exchange': self.exchange,
			'curr_type': self.curr_type,
			'list_status': self.list_status,
			'list_date': self.list_date,
			'delist_date': self.delist_date,
			'is_hs': self.is_hs,
			'price': self.price,
			'circ_mv': self.circ_mv,
			'pe': self.pe,
		}

	def __repr__(self):
		return '<Stock %r>' % self.name

class Day(db.Model):
	__tablename__='days'
	id = db.Column(db.Integer, primary_key=True)
	trade_date = db.Column(db.Date)
	close = db.Column(db.Float)
	turnover_rate = db.Column(db.Float)
	turnover_rate_f = db.Column(db.Float)
	volume_ratio = db.Column(db.Float)
	pe = db.Column(db.Float)
	pe_ttm = db.Column(db.Float)
	pb = db.Column(db.Float)
	ps = db.Column(db.Float)
	ps_ttm = db.Column(db.Float)
	dv_ratio = db.Column(db.Float)
	dv_ttm = db.Column(db.Float)
	total_share = db.Column(db.Float)
	float_share = db.Column(db.Float)
	free_share = db.Column(db.Float)
	total_mv = db.Column(db.Float)
	circ_mv = db.Column(db.Float)
	stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
	stock = db.relationship('Stock', backref=db.backref('days', lazy='dynamic'))
	
	def to_json(self):
		return{
			'id':self.id,
			'trade_date': self.trade_date,
			'close': self.close,
			'turnover_rate': self.turnover_rate,
			'turnover_rate_f': self.turnover_rate_f,
			'volume_ratio': self.volume_ratio,
			'pe': self.pe,
			'pe_ttm': self.pe_ttm,
			'pb': self.pb,
			'ps': self.ps,
			'ps_ttm': self.ps_ttm,
			'dv_ratio': self.dv_ratio,
			'dv_ttm': self.dv_ttm,
			'total_share': self.total_share,
			'float_share': self.float_share,
			'free_share': self.free_share,
			'total_mv': self.total_mv,
			'circ_mv': self.circ_mv,
			'stock_name' : self.stock.name,
		}

	def __repr__(self):
		return '<Day %r>' % self.name

GroupStock = db.Table('groupstocks',
	db.Column('group_id',db.Integer,db.ForeignKey('groups.id')),
	db.Column('stock_id',db.Integer,db.ForeignKey('stocks.id')))

class Group(db.Model):
	__tablename__='groups'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	
	def to_json(self):
		return{
			'id':self.id,
			'name': self.name,
		}

	def __repr__(self):
		return '<Group %r>' % self.name
