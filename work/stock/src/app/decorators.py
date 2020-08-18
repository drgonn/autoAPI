
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
