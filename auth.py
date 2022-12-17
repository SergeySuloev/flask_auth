from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_user, login_required, logout_user
from models import Users, LoginForm, SignupForm
from app import db, bcrypt

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('views.welcome'))
                else:
                    flash("Wrong password.")
            else:
                flash("User doesn't exist.")
        else:
            flash('Invalid username or password.')

    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            print('DEBUG | Created new user')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or password.')

    return render_template('signup.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
