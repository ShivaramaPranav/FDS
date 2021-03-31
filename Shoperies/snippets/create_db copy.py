#
# Use this to create a DB
#
from flask import Flask, render_template_string, request
from flask_mail import Mail

from flask_sqlalchemy  import SQLAlchemy
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask_user import roles_required
from flask_talisman import Talisman
from web.models import *
from web import db

#admin1 = Admin(username='admin', email='admin@admin.com', password='admin', phone_no='384734877')
app = Flask(__name__)
Talisman(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba254'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sxpwlhvvkffvkj:09fe494ff2350a489fb95d1c7ff6f8710b61f99efb8cce5910142646415b432e@ec2-52-2-82-109.compute-1.amazonaws.com:5432/d9c8sa7jk8bbii'
app.config['DEBUG'] = True
db_adapter = SQLAlchemyAdapter(db,  User)
user_manager = UserManager(db_adapter, app)
user1 = User(username='test3', email='blahet@blah.com', phone_no='543216',password=user_manager.hash_password('xyza'), is_working=True)
db.session.add(user1)
db.session.commit()