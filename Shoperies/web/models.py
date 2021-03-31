from enum import Enum
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from web import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_users(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_no = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_working = db.Column(db.Boolean, nullable=False, default=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    
    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})
    def __repr__(self):
        return f"User('{self.id}', '{self.phone_no}', '{self.username}', '{self.email}', '{self.is_working}')"

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
    user = db.relationship('Role')

class OrderStatus(Enum):
    accepted = 'Order Accepted'
    cooking = 'Preparing your meal'
    eta_30 = 'Your Order is 30 Minutes Away'
    eta_10 = 'Your Order is 10 Minutes Away'
    reached = 'Your Order has reached your location'
    delivered = 'Order Delivered'
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        item = cls(item) \
            if not isinstance(item, cls) \
            else item  # a ValueError thrown if item is not defined in cls.
        return item.value
    
    def __str__(self):
        return str(self.value)

class Order(db.Model, UserMixin):
    __tablename__ = 'orders'
    # Order Details
    id = db.Column(db.Integer, primary_key=True)
    # metadata
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.accepted)
    # User/Agent details
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user', lazy='dynamic'))
    user_tip = db.Column(db.Float, default=0.0)
    # Customer details
    cust_name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    cust_addr1 = db.Column(db.String(65), nullable=False)
    cust_addr2 = db.Column(db.String(65), nullable=True)
    cust_pincode = db.Column(db.String(12), nullable=False)
    #Delivery Details
    delivery_instructions = db.Column(db.String(300), nullable=True)
