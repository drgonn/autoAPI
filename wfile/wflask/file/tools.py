
import base64
import hashlib
import hmac
import logging
from datetime import datetime
from time import time

import jwt
import requests
from dateutil import tz
from dateutil.tz import tzlocal
from flask import current_app, g
from jwt import exceptions

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
	print(token)
	result = {'status': False, 'data': None, 'error': None}
	try:
		verified_payload = jwt.decode(token, current_app.config['SECRET_KEY'], True)
		result['status'] = True
		result['data'] = verified_payload
	except exceptions.ExpiredSignatureError:
		result['error'] = 'token已失效'
	except jwt.DecodeError:
		result['error'] = 'token认证失败'
	except jwt.InvalidTokenError:
		result['error'] = '非法的token'
	print(result)
	return result['data']


def getinusedevice(uid):        #获取有任务设备ID列表
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
    
    
	
