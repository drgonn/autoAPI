
import flask_admin as admin
from .views import *
from app.models import *
admin = admin.Admin(name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Stock, db.session))
admin.add_view(ModelView(Day, db.session))
admin.add_view(ModelView(Group, db.session))
