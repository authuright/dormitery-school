
from flask import render_template,url_for,redirect,request
import flask
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db,login_manager
from apps.authentication import blueprint
from apps.authentication.models import Users
from apps.authentication.forms import LoginForm, CreateAccountForm

from apps.authentication.util import hash_pass,verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm(request.form)
    if flask.request.method == 'POST':
        # read form data
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        
        if user and verify_pass(password,user.password):
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))
        
        return render_template('accounts/login.html',
                                msg='Wrong user or password',
                                form=login_form)
        
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    else:
        return render_template('accounts/login.html',
                               form=login_form) 

@blueprint.route('/register', methods=['GET','POST'])
def register():
    register_form = CreateAccountForm(request.form)
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form = register_form)
            
        user = Users.query.filter_by(email=email).first()  
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form = register_form)
        password = hash_pass(password)
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()
        
        # Delete user from session
        logout_user()
        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=register_form)
        
    return render_template('accounts/register.html', form = register_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/error.html',msg="Unauthorized Template"), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/error.html',msg="access_forbidden"), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/error.html',msg="not_found_error"), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/error.html',msg="internal_error"), 500