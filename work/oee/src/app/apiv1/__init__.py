from flask import Blueprint
api = Blueprint('api', __name__)
from app.apiv1 import auth, Device, public, Role, Userlog, Valve, Worktime