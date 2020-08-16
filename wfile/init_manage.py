import os
from tools import Tdb


def write_init(root,ojson):
    flaskapscheduler = ojson.get('Flask_APScheduler')
    appname = ojson.get('app')
    initdir = os.path.join(root,f'{appname}/src/__init__.py')
    w = open(initdir,'w+')
    w.write('import os')
    w.write("\n")
    w.write('import redis')
    w.write('from flask import Flask')
    w.write('from flask_sqlalchemy import SQLAlchemy')
    w.write('from flask_cors import CORS')
    w.write('from flask_mail import Mail')
    w.write('from celery import Celery')
    w.write('from flasgger import Swagger')
    w.write('from flask_admin import Admin, BaseView, expose')
    w.write('from flask_apscheduler import APScheduler')
    w.write('from apscheduler.schedulers.background import BackgroundScheduler') 
    w.write("\n")
    w.write('from config import config')
    w.write('from app.admin import admin')
    w.write("\n")
    w.write('db = SQLAlchemy()')
    w.write('swagger = Swagger()')
    w.write('celery = Celery()')
    w.write('mail = Mail()')

    w.write('scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))')
    w.write('scheduler.init_app(app)')


    w.write('scheduler.start()')



    w.write('def create_app(config_name = "default"):')
    w.write('\tapp = Flask(__name__, static_url_path="")')
    w.write('\tapp.config.from_object(config[config_name])')
    w.write('\tconfig[config_name].init_app(app)')
    w.write('\tmail.init_app(app)')
    w.write('\tdb.init_app(app)')
    w.write('\tswagger.init_app(app)')
    w.write('\tCORS(app, supports_credentials=True)')
    w.write('\tpool = redis.ConnectionPool(host = app.config["REDIS_HOST"], port = app.config["REDIS_PORT"], decode_responses = True)')
    w.write('\tapp.sredis = redis.StrictRedis(connection_pool = pool)')
    w.write('\tapp.sredisPipe = app.sredis.pipeline(transaction = True)')
    w.write('\tcelery.conf.update(app.config)')
    w.write('\tadmin.init_app(app)')
    w.write('\tfrom app.apiv1 import api as api_blueprint')
    w.write('\tapp.register_blueprint(api_blueprint, url_prefix="/api/v1/order")')
    w.write('\treturn app')

    w.close()





