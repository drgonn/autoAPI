
import flask_admin as admin
from .views import *
from app.models import *
admin = admin.Admin(name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Device, db.session))
admin.add_view(ModelView(Worktime, db.session))
admin.add_view(ModelView(Valve, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Usercopy, db.session))
admin.add_view(ModelView(Userlog, db.session))
