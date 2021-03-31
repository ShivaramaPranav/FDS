from flask import Blueprint, render_template,redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import *
from . import db, bcrypt
from flask import Flask, render_template
from flask_login import login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')    
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=True)
    #TODO: Handle case when role is empty
    #currently agent is not assigned any role by default
    if user.roles[0].name == 'Admin':
        return redirect(url_for('main.da_list'))
    else:
        return redirect(url_for('main.agent_view'))

@auth.route('/reset_password', methods=['POST'])
def reset_password():
    current_password = request.form.get('current_password')    
    updated_password = request.form.get('updated_password')
    confirm_updated_password = request.form.get('confirm_updated_password')
    user = User.query.filter_by(email=current_user.email).first()
    if not user or not bcrypt.check_password_hash(user.password, current_password): 
        flash('The current password you entered is wrong')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=True)
    #TODO: Handle case when role is empty
    #currently agent is not assigned any role by default
    if user.roles[0].name == 'Admin':
        return redirect(url_for('main.da_list'))
    else:
        return redirect(url_for('main.agent_view'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('username')
    email = request.form.get('email')    
    password = request.form.get('password')
    confirm_password = request.form.get('confirmpassword')
    phonenumber = request.form.get('phonenumber')

    if password != confirm_password:
        flash("Passwords don't match!")
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(email=email).first() 

    if user:
        flash('Email address already exists, please login!')
        return redirect(url_for('auth.signup'))
    
    default_role = Role.query.filter_by(name='Agent').first()
    new_user = User(username=name, email=email, phone_no=phonenumber, password=bcrypt.generate_password_hash(password).decode('utf-8'), is_working=True)
    new_user.roles.append(default_role)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))