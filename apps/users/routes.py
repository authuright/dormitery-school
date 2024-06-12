from flask import Flask,render_template,redirect,url_for
from apps.users import blueprint



@blueprint.route('/user')
def user_view():
    return render_template('user/user.html')