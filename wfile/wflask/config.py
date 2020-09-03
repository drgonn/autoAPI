import os
from tools import Tdb


#建立models
def write_config(root,ojson):
    dataname = ojson.get('dataname')
    datapassword = ojson.get('datapassword')
    flaskapscheduler = ojson.get('Flask_APScheduler')


    appname = ojson.get('app')
    initdir = os.path.join(root, f'{appname}/src/config.py')
    w = open(initdir, 'w+')
    w.write(f'import os\n')
    w.write(f'basedir = os.path.abspath(os.path.dirname(__file__))\n')
    w.write(f'from datetime import timedelta\n')
    w.write(f'from celery.schedules import crontab\n')
    if flaskapscheduler:
        w.write(f'from app.tasks import JOBS \n')
    w.write(f'\n')
    w.write(f'class Config:\n')
    w.write(f'	SECRET_KEY = os.environ.get("SECRET_KEY") or "2d21c91217794dc687100033cf2e47c9"\n')
    w.write(f'	SSL_REDIRECT = False\n')
    w.write(f'	SQLALCHEMY_TRACK_MODIFICATIONS = False\n')
    w.write(f'	SQLALCHEMY_RECORD_QUERIES = True\n')
    w.write(f'	PER_PAGE = 20\n')
    w.write(f'	FLASKY_SLOW_DB_QUERY_TIME = 0.5\n\n')
    if flaskapscheduler:
        w.write(f'	SCHEDULER_API_ENABLED = True\n')
        w.write(f'	SCHEDULER_TIMEZONE = "Asia/Shanghai"\n')
        w.write(f'	JOBS = JOBS\n')
    w.write(f'\n')
    w.write(f'\n')
    w.write(f'	@staticmethod\n')
    w.write(f'	def init_app(app):\n')
    w.write(f'		pass\n')
    w.write(f'		\n')
    w.write(f'class DevelopmentConfig(Config):\n')
    w.write(f'	DEBUG = True\n')
    w.write(f'	MAIN_HOST = os.environ.get("MAIN_HOST") or "http://127.0.0.1:5001"\n')
    w.write(f'	# Redis configuration\n')
    w.write(f'	REDIS_HOST = "localhost"\n')
    w.write(f'	REDIS_PORT = 6379\n')
    w.write(f'	# Celery configuration\n')
    w.write(f'	BROKER_URL = "redis://localhost:6379/0"\n')
    w.write(f'	CELERY_RESULT_BACKEND = "redis://localhost:6379/0"\n')
    w.write(f'	# Database configuration\n')
    w.write(f'	SQL_NAME = os.environ.get("SQL_NAME") or "root"\n')
    w.write(f'	SQL_PASSWORD = os.environ.get("SQL_PASSWORD") or "{datapassword}"\n')
    w.write(f'	SQL_HOST = os.environ.get("SQL_HOST") or "127.0.0.1:3306"\n')
    w.write(f'	SQL_DATABASE = os.environ.get("SQL_DATABASE") or "{dataname}"\n')
    w.write(f'	SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{{SQL_NAME}}:{{SQL_PASSWORD}}@{{SQL_HOST}}/{{SQL_DATABASE}}"\n')
    w.write(f'\n')
    w.write(f'	# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:7811175yy@127.0.0.1:3306/dcv3qiot"\n')
    w.write(f'\n')
    w.write(f'\n')
    w.write(f'\n')
    w.write(f'	INFLUX_USERNAME = os.environ.get("INFLUX_USERNAME") or  "admin"\n')
    w.write(f'	INFLUX_PASSWORD = os.environ.get("INFLUX_PASSWORD") or  "668899"\n')
    w.write(f'	INFLUX_DBNAME   = os.environ.get("INFLUX_DBNAME") or  "db0"\n')
    w.write(f'	INFLUX_HOST     = os.environ.get("INFLUX_HOST") or  "influxdb"\n')
    w.write(f'	OTA_URL = os.environ.get("OTA_URL") or "127.0.0.1"\n')
    w.write(f'	OTA_URL_ALL = f"http://{{OTA_URL}}:5010"\n')
    w.write(f'	QIOT_HOST = os.environ.get("QIOT_HOST") or  "0.0.0.0:5001"\n')
    w.write(f'	QIOT_URL = os.environ.get("QIOT_URL") or "https://iot.sealan.tech/mina/"\n')
    w.write(f'\n')
    w.write(f'\n')
    w.write(f'class TestingConfig(Config):\n')
    w.write(f'	TESTING = True\n')
    w.write(f'	# Redis configuration\n')
    w.write(f'	REDIS_HOST = "localhost"\n')
    w.write(f'	REDIS_PORT = 6379\n')
    w.write(f'	# Celery configuration\n')
    w.write(f'	BROKER_URL = "redis://localhost:6379/0"\n')
    w.write(f'	CELERY_RESULT_BACKEND = "redis://localhost:6379/0"\n')
    w.write(f'	# Database configuration\n')
    w.write(f'	SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \\\n')
    w.write(f'		"mysql+pymysql://root:7811175yy@127.0.0.1:3306/test"\n')
    w.write(f'	WTF_CSRF_ENABLED = False\n')
    w.write(f'	QIOT_URL = os.environ.get("QIOT_URL") or "https://iot.sealan.tech/mina/"\n')
    w.write(f'\n')
    w.write(f'\n')
    w.write(f'\n')
    w.write(f'class ProductionConfig(Config):\n')
    w.write(f'	MAIN_HOST = os.environ.get("MAIN_HOST") or "https://qiot.sealan-tech.com"\n')
    w.write(f'\n')
    w.write(f'	# Redis configuration\n')
    w.write(f'	REDIS_HOST = os.environ.get("REDIS_HOST") or "redis"\n')
    w.write(f'	REDIS_PORT = os.environ.get("REDIS_PORT") or 6379\n')
    w.write(f'	REDIS_DEV  = os.environ.get("REDIS_DEV") or 0\n')
    w.write(f'	# Celery configuration\n')
    w.write(f'	BROKER_URL = f"redis://{{REDIS_HOST}}:{{REDIS_PORT}}/{{REDIS_DEV}}"\n')
    w.write(f'	CELERY_RESULT_BACKEND = f"redis://{{REDIS_HOST}}:{{REDIS_PORT}}/{{REDIS_DEV}}"\n')
    w.write(f'	# Database configuration\n')
    w.write(f'	SQL_NAME = os.environ.get("SQL_NAME") or "root"\n')
    w.write(f'	SQL_PASSWORD = os.environ.get("SQL_PASSWORD") or "668899"\n')
    w.write(f'	SQL_HOST = os.environ.get("SQL_HOST") or "172.17.0.5"\n')
    w.write(f'	SQL_DATABASE = os.environ.get("SQL_DATABASE") or "{dataname}"\n')
    w.write(f'	SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{{SQL_NAME}}:{{SQL_PASSWORD}}@{{SQL_HOST}}/{{SQL_DATABASE}}"\n')
    w.write(f'\n')
    w.write(f'	ROLE_IP = os.environ.get("ROLE_IP")   or "127.0.0.1"\n')
    w.write(f'	ROLE_PORT = os.environ.get("ROLR_PORT") or "50051"\n')
    w.write(f'\n')
    w.write(f'	INFLUX_USERNAME = os.environ.get("INFLUX_USERNAME") or  "admin"\n')
    w.write(f'	INFLUX_PASSWORD = os.environ.get("INFLUX_PASSWORD") or  "668899"\n')
    w.write(f'	INFLUX_DBNAME   = os.environ.get("INFLUX_DBNAME") or  "db0"\n')
    w.write(f'	INFLUX_HOST     = os.environ.get("INFLUX_HOST") or  "influxdb"\n')
    w.write(f'	QIOT_HOST = os.environ.get("QIOT_HOST") or  "dc.sealan-tech.com"\n')
    w.write(f'	QIOT_URL = os.environ.get("QIOT_URL") or "https://iot.sealan.tech/mina/"\n')
    w.write(f'\n')
    w.write(f'config = {{\n')
    w.write(f'	"development": DevelopmentConfig,\n')
    w.write(f'	"testing": TestingConfig,\n')
    w.write(f'	"production": ProductionConfig,\n')
    w.write(f'	"default": DevelopmentConfig\n')
    w.write(f'}}\n')

    w.close()
















