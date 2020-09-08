import os
from tools import Tdb


def write_init(root,ojson):
    flaskapscheduler = ojson.get('Flask_APScheduler')
    auth = ojson.get('auth')
    appname = ojson.get('app')
    initdir = os.path.join(root,f'{appname}/src/app/__init__.py')
    w = open(initdir,'w+')
    w.write('import os\n')
    w.write("\n")
    w.write('import redis\n')
    w.write('from flask import Flask\n')
    w.write('from flask_sqlalchemy import SQLAlchemy\n')
    w.write('from flask_cors import CORS\n')
    w.write('from flask_mail import Mail\n')
    w.write('from celery import Celery\n')
    w.write('from flasgger import Swagger\n')
    w.write('from flask_admin import Admin, BaseView, expose\n')
    if flaskapscheduler:
        w.write('from flask_apscheduler import APScheduler\n')
        w.write('from apscheduler.schedulers.background import BackgroundScheduler')
    w.write("\n")
    w.write('from config import config\n')
    w.write("\n")
    w.write('db = SQLAlchemy()\n')
    w.write('swagger = Swagger()\n')
    w.write('celery = Celery()\n')
    w.write('mail = Mail()\n')

    if flaskapscheduler:
        w.write('scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))\n')
    w.write('def create_app(config_name = "default"):\n')
    w.write('\tapp = Flask(__name__, static_url_path="")\n')
    w.write('\tapp.config.from_object(config[config_name])\n')
    w.write('\tconfig[config_name].init_app(app)\n')
    w.write('\tmail.init_app(app)\n')
    w.write('\tdb.init_app(app)\n')
    w.write('\tswagger.init_app(app)\n')
    if flaskapscheduler:
        w.write('\tscheduler.init_app(app)\n')
        w.write('\tscheduler.start()\n')
    w.write('\tCORS(app, supports_credentials=True)\n')
    w.write('\tpool = redis.ConnectionPool(host = app.config["REDIS_HOST"], port = app.config["REDIS_PORT"], decode_responses = True)\n')
    w.write('\tapp.sredis = redis.StrictRedis(connection_pool = pool)\n')
    w.write('\tapp.sredisPipe = app.sredis.pipeline(transaction = True)\n')
    w.write('\tcelery.conf.update(app.config)\n')
    w.write('\tfrom app.apiv1 import api as api_blueprint\n')
    w.write(f'\tapp.register_blueprint(api_blueprint, url_prefix="/api/v1/{appname}")\n')
    w.write('\treturn app\n')

    w.close()

    # 本地测试启动脚本
    initdir = os.path.join(root,f'{appname}/src/run_manage.sh')
    w = open(initdir,'w+')
    test_port = ojson.get('testport')
    w.write(f'python3 manage.py runserver --port {test_port}')
    w.close()


    # 写本地启动脚本
    initdir = os.path.join(root,f'{appname}/src/manage.py')
    w = open(initdir,'w+')


    w.write('import os\n')
    w.write('from flask_script import Manager, Shell\n')
    w.write('from flask_migrate import Migrate, MigrateCommand\n')
    w.write('from app import create_app, db, celery\n')
    w.write('from app.models import  *\n')
    w.write('app = create_app(os.getenv("FLASK_CONFIG") or "default")\n')
    w.write('manager = Manager(app)\n')
    w.write('migrate = Migrate(app, db)\n')
    w.write('app.app_context().push()\n')
    w.write('def make_shell_context():\n')
    w.write('\treturn dict(app=app,db=db')

    for table in ojson.get('databases'):
        tableclass = table.get('table')
        w.write(f',{tableclass} = {tableclass}')
    w.write(')\n')
    w.write('manager.add_command("shell", Shell(make_context=make_shell_context))\n')
    w.write('manager.add_command("db", MigrateCommand)\n')
    w.write('@manager.command\n')
    w.write('def db_init():\n')
    w.write('\tdb.create_all()\n')
    w.write('@manager.command \n')
    w.write('def test():\n')
    w.write('\timport unittest\n')
    w.write('\ttests = unittest.TestLoader().discover("tests")\n')
    w.write('\tunittest.TextTestRunner(verbosity=2).run(tests)\n')
    w.write('if __name__ == "__main__":\n')
    w.write('\tmanager.run()\n')
    w.close()
