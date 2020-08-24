import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db, celery
from app.models import  *
app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)
app.app_context().push()
def make_shell_context():
	return dict(app=app,db=db,Stock = Stock,Day = Day,Group = Group)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
@manager.command
def db_init():
	db.create_all()
@manager.command 
def test():
	import unittest
	tests = unittest.TestLoader().discover("tests")
	unittest.TextTestRunner(verbosity=2).run(tests)
@manager.command 
def init_base():
	appnames = ["card","qiot"]
	for name in appnames:
		if App.query.filter_by(name=name).first() is None:
			app = App(name=name)
			db.session.add(app)
	db.session.commit()
	cardtype=["续费订单"]
	app =  App.query.filter_by(name="card").first()
	for tname in cardtype:
		if OType.query.filter_by(name=name).first() is None:
			type = OType(name=name,app=app)
			db.session.add(type)
	db.session.commit()
if __name__ == "__main__":
	manager.run()
