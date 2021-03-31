import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'eibccckhvccjlcivhjggujflbifrucgirbbgebtgvnfr'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://sxpwlhvvkffvkj:09fe494ff2350a489fb95d1c7ff6f8710b61f99efb8cce5910142646415b432e@ec2-52-2-82-109.compute-1.amazonaws.com:5432/d9c8sa7jk8bbii')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.environ.get('DEBUG_FLAG', False)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)
bootstrap = Bootstrap(app)

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_roles('Admin')

admin = Admin(app, name='Admin', template_mode='bootstrap4', index_view=MyAdminIndexView())



# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .models import *
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(UserRoles, db.session))
admin.add_view(ModelView(Order, db.session))

db_adapter = SQLAlchemyAdapter(db,  User)
user_manager = UserManager(db_adapter, app, login_view_function=auth.login, logout_view_function=auth.logout)
