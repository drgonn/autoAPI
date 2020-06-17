import os
def write_admin(root,ojson):
    appname = ojson.get('app')

    initdir = os.path.join(root,f'{appname}/src/app/admin/__init__.py')
    w = open(initdir,'w+')
    w.write(admininit)
    for table in ojson.get('databases'):
        w.write(f"admin.add_view(ModelView({table.get('table')}, db.session))\n")

    w.close()

    initdir = os.path.join(root,f'{appname}/src/app/admin/views.py')
    w = open(initdir,'w+')
    w.write(views)
    w.close()


admininit = """
import flask_admin as admin
from .views import *
from app.models import *
admin = admin.Admin(name='Admin', template_mode='bootstrap3')
"""
views = """
from flask_admin.contrib import sqla
class ModelView(sqla.ModelView):
	pass
"""
