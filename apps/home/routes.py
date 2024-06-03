

from apps.home import blueprint
from flask import render_template,request
from flask_login import login_required
@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html')