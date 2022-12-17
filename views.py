from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/welcome')
@login_required
def welcome():
    return render_template("welcome.html", user=current_user.username)
