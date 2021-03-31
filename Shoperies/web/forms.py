from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import *
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web.models import User, OrderStatus
from wtforms.fields.html5 import *
from datetime import datetime, date
from flask_login import login_required, current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class OrderItemsForm(FlaskForm):
    status = SelectField('Status of Order', choices=OrderStatus.choices())
    cust_name = StringField('Customer Name', validators=[DataRequired(), Length(min=3, max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(10)])
    cust_addr1 = TextAreaField('Address Line 1', validators=[DataRequired(), Length(min=5, max=65)],  render_kw={'class': 'form-control', 'rows': 5, 'cols':5})
    cust_addr2 = TextAreaField('Address Line 2', validators=[Length(min=0, max=65)],  render_kw={'class': 'form-control', 'rows': 5, 'cols':5})
    cust_pincode = StringField('Pin Code', validators=[DataRequired(), Length(min=5, max=12)])
    user_tip = FloatField('Tip', default=0)
    delivery_instructions = TextAreaField('Delivery Instructions',  render_kw={'class': 'form-control', 'rows': 5, 'cols':5}, validators=[Length(min=0, max=300)])
    submit = SubmitField('Add Order')
    # delivery_date = DateField('Delivery Date', format='%Y-%m-%d',  validators=[DataRequired()])
    # delivery_start_time = TimeField('Start Time')
    # delivery_end_time = TimeField('End Time')
    
    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('length should be less than 16')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('failed validating with +1')

class ResetPasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6, max=20)])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password')])
    confirm_new_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_current_password(self, current_password):
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
