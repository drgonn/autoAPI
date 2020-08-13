import os
from tools import Tdb


#建立models
def make_init(root,ojson):
    appname = ojson.get('app')
    initdir = os.path.join(root,f'{appname}/src/__init__.py')
    w = open(initdir,'w+')
    w.close()

    initdir = os.path.join(root,f'{appname}/src/app/decorators.py')
    w = open(initdir,'w+')
    w.write(decorators)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/app/tools.py')
    w = open(initdir,'w+')
    w.write(tools)
    w.close()
    initdir = os.path.join(root,f'{appname}/requirements.txt')
    w = open(initdir,'w+')
    w.write(requirements)
    w.close()
    initdir = os.path.join(root,f'{appname}/.gitignore')
    w = open(initdir,'w+')
    w.write(gitignore)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/wsgi.py')
    w = open(initdir,'w+')
    w.write(wsgi)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/start.sh')
    w = open(initdir,'w+')
    w.write(start)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/public.crt')
    w = open(initdir,'w+')
    w.write(public)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/private.pem')
    w = open(initdir,'w+')
    w.write(private)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/manage.py')
    w = open(initdir,'w+')
    w.write(manage)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/gunicorn.conf.py')
    w = open(initdir,'w+')
    w.write(gunicorn)
    w.close()
    initdir = os.path.join(root,f'{appname}/Dockerfile')
    w = open(initdir,'w+')
    w.write(dockerfile)
    w.close()
    initdir = os.path.join(root,f'{appname}/src/app/standard.py')
    w = open(initdir,'w+')
    w.write(standard)
    w.close()



decorators = """
from functools import wraps
from flask import abort,g
# from flask_login import current_user
from app.models import Permission
from app.tools import get_permission
#用作权限访问的装饰器
def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not get_permission(permission):
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator
def admin_required(f):
	return permission_required(Permission.ADMIN)(f)
"""
tools = """
import hashlib
import requests
from dateutil import tz
from dateutil.tz import tzlocal
from datetime import datetime
from time import time
import base64
import hmac
import logging

from flask import current_app,g
from authlib.jose import jwt

permission_dir = {"one":1,"two":3,"three":7,"four":15,"five":31}
#生成散列
def md5(arg):#这是加密函数，将传进来的函数加密
    md5_pwd = hashlib.md5(bytes(arg,encoding='utf-8'))
    md5_pwd.update(bytes("chenrong",encoding='utf-8'))
    return md5_pwd.hexdigest()#返回加密的数据
# 生成随机散列
def randomd5():
	return md5(str(time()))
'''
 utc时间转本地时间,并转换为字符
'''
def utc_switch(utc,time_zone="GTM+8"):
	if utc:
		time_zone = time_zone or "GTM+8"
		local_zone = time_zone or datetime.now(tzlocal()).tzname()
		# UTC Zone
		from_zone = tz.gettz('UTC')
		# China Zone
		to_zone = tz.gettz(local_zone)
		utc = utc.replace(tzinfo=to_zone)
		local = utc.astimezone(from_zone)
		return datetime.strftime(local, "%Y-%m-%d %H:%M:%S")
def generate_token(key,id, expire=3600):
	ts_str = str(time() + expire)
	ts_byte = ts_str.encode("utf-8")
	sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
	token = ts_str + ':' + sha1_tshexstr + ':' + str(id)
	b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
	return b64_token.decode("utf-8")
# 验证token
def certify_token(token):
	key = open('public.crt', 'r').read()
	try:
		token_dir = jwt.decode(token, key)
	except Exception as e:
		logging.error(e)
		logging.error(f"token解码错误，token是: {token}")
	return token_dir
def get_trole(token):
	key = open('public.crt','r').read()
	token_dir = jwt.decode(token, key)
	return token_dir.get('role')
def getinusedevice(uid):        #获取有任务设备ID列表
	print('getinuserddddddddddddddddd')
	murl = current_app.config["OTA_URL_ALL"]
	url = f'{murl}/api/v1/firmware/jump/inuse/deviceids'
	logging.error(url)
	r = requests.request("post", url, json={"uid": uid}).json()
	print(r)
	if r.get("ret"):
		return r.get("data")
def get_permission(permission):
	role_permission = permission_dir.get(g.role)
	return role_permission & permission == permission
def is_admin():
	return get_permission(16)
def verify_auth_token(token):
    uid = certify_token(token)
    if uid:
        return User.query.filter_by(uid=uid).first()
    else:
        return None
    
    
	
"""
requirements = """
alembic==1.0.11
amqp==2.4.1
aniso8601==4.1.0
asn1crypto==0.24.0
Authlib==0.14.1
billiard==3.5.0.5
blinker==1.4
celery==4.2.1
certifi==2019.6.16
cffi==1.12.0
chardet==3.0.4
Click==7.0
cryptography==2.5
Django==2.2.5
dominate==2.3.5
flasgger==0.9.3
Flask==1.1.1
Flask-Admin==1.5.3
Flask-Cors==3.0.8
Flask-HTTPAuth==3.2.3
Flask-Login==0.4.1
Flask-Mail==0.9.1
Flask-Migrate==2.5.2
Flask-RESTful==0.3.7
Flask-Script==2.0.6
Flask-SQLAlchemy==2.4.0
Flask-WTF==0.14.2
ForgeryPy==0.1
gevent==1.4.0
greenlet==0.4.15
grpcio==1.24.1
grpcio-tools==1.24.1
gunicorn==19.9.0
httpie==0.9.9
idna==2.8
image==1.5.27
influxdb==5.2.3
itsdangerous==0.24
Jinja2==2.10.1
jmespath==0.9.3
jsonschema==2.6.0
kombu==4.3.0
Mako==1.1.0
MarkupSafe==1.1.1
mistune==0.8.4
Pillow==6.0.0
protobuf==3.10.0
pycparser==2.19
pycryptodome==3.7.3
Pygments==2.2.0
PyMySQL==0.9.3
python-dateutil==2.8.0
python-editor==1.0.4
pytz==2018.9
PyYAML==5.1.2
qrcode==6.1
redis==3.3.6
requests==2.22.0
six==1.12.0
SQLAlchemy==1.3.6
sqlparse==0.3.0
urllib3==1.25.3
vine==1.2.0
visitor==0.1.3
Werkzeug==0.16.0
WTForms==2.2.1
xlrd==1.1.0
xlwt==1.3.0
"""
gitignore = """
__pycache__/
*.py[cod]
*$py.class
env/
.idea/
src/app/static/
"""
wsgi = """
# -*- coding: utf-8 -*-
from flask import Flask
from app import create_app, celery
app = create_app("production")
app.app_context().push()
if __name__ == '__main__':
	app.run()
"""
start = """#!/bin/bash
python manage.py db upgrade
python manage.py redis
python manage.py init_base
gunicorn  wsgi:app  -c  ./gunicorn.conf.py
"""
public = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDSPUCy5JSapWXu0afnFx74CBVj
kkN5GhiVIF/unBy89ds7qO3JCVw5CbUG84F5vb7ncroZkKrbgIeHFem2NZ8+vDzl
jIlcnPT/Rc3QIY2WdOQ6braOAt4O+Oefq8v6oe4RERzfcwInOszvNZeYpZNkGtDL
SAK7sdcTjohxm3Ik5QIDAQAB
-----END PUBLIC KEY-----
"""
private = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDSPUCy5JSapWXu0afnFx74CBVjkkN5GhiVIF/unBy89ds7qO3J
CVw5CbUG84F5vb7ncroZkKrbgIeHFem2NZ8+vDzljIlcnPT/Rc3QIY2WdOQ6braO
At4O+Oefq8v6oe4RERzfcwInOszvNZeYpZNkGtDLSAK7sdcTjohxm3Ik5QIDAQAB
AoGAUpUK5/pPwRs9Gf0ytdxoJseOF0mpxVUR2OoZpLGfvD3auumVVcWeey0r9aoK
7tYwudtf7JDd/FDVa6OY5SDVBupFq7A8zwarPuQAttiwPHDlE/4OdcKKqICGQJfI
6g/e6f0UbuCWFiOFxhWXei+C6AwH1lhJySaH5IuPZ+twwoECQQDrL2IwtQ1oY1CO
sIYlGCdqHtCoXwRf0niFUKG8ZeRTVlt9OUWb2Ngmq/z6mv3692rNfOMVR2OI8+FT
hR91lSoFAkEA5NirL+jhwIEy7ypOy5dDdElbdp9q/36idm0qFpCe/uDNaiNYZVZo
42vw9DJQ/PVWzOgBiQ7sUaY8aLzwcfilYQJBAMXmUl6gC086uu/G9KpEH+55TaVQ
hxLGvWmZBu/MYYwKz+OYjM1uc7xe3vpV77/98B5Hp6IhN01nwsSP8X/0660CQQC0
3HR22dPJQ5LQqBw8FSEvf2Z02stCf3/Ansf7q3KtN1fBAYw0EtW0nzOAm1+ce/2M
1fOYsZ2dbgciM+jH+l4hAkATg7kgwMONxn0i+AA0hszKgPzxj7Bvk2E9DLeNtryo
ghCU2TwwHrBWws/Wv1GucTm3idoIYg5kq7F8qKZBMfQ9
-----END RSA PRIVATE KEY-----
"""
manage = """
#!/usr/bin/env python
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db, celery
from app.models import  *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
app.app_context().push()

def make_shell_context():
	return dict(app=app,db=db,User=User,App=App,)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def db_init():
	db.create_all()

@manager.command 
def test():
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command 
def init_base():
	appnames = ['card','qiot']
	for name in appnames:
		if App.query.filter_by(name=name).first() is None:
			app = App(name=name)
			db.session.add(app)
	db.session.commit()
	cardtype=["续费订单"]
	app =  App.query.filter_by(name='card').first()
	for tname in cardtype:
		if OType.query.filter_by(name=name).first() is None:
			type = OType(name=name,app=app)
			db.session.add(type)
	db.session.commit()


if __name__ == "__main__":
	manager.run()
"""
gunicorn = """
workers = 5    # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent"   # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:5050"    # 监听IP放宽，以便于Docker之间、Docker和宿主机之间的通
errorlog = '/code/log/gunicorn.error.log'
accesslog = '/code/log/gunicorn.access.log'
"""
dockerfile = """
FROM python:3.6.2
RUN mkdir /code
RUN mkdir /code/log
WORKDIR /code
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/gunicorn.conf.py ./
COPY src/start.sh ./
COPY . .
WORKDIR /code/src
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
"""
standard = """
class Permission:
    USER = 1
    MANAGE_USER = 2
    MANAGE_AGENCY =4
    ADMIN = 16
"""
