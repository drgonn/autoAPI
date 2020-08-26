from flask import Blueprint
api = Blueprint('api', __name__)
from app.apiv1 import auth, Day, Group, Stock, stock_day, update