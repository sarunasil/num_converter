from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from . import db
from .models import User

PASSWORD_MIN_LEN = 8

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for( 'main.index' ))

    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Incorrect login details.','is-danger')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/register')
@login_required
def register():
    #only admin can register new users
    if current_user.typee != 1:
        flash("Only admin can register new users", 'is-danger')
        return redirect(url_for('main.index'))

    return render_template('auth/register.html')

@auth.route('/register', methods=['POST'])
@login_required
def register_post():
    #only admin can register new users
    if current_user.typee != 1:
        flash("Only admin can register new users", 'is-danger')
        return redirect(url_for('main.index'))

    username = request.form.get('username')
    password = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(username=username).first()
    if user:
        flash('User already exists.', 'is-danger')
        return redirect(url_for('auth.register'))
    elif password != password2:
        flash("Passwords do not match.", 'is-danger')
        return redirect(url_for('auth.register'))
    elif len(password) < PASSWORD_MIN_LEN:
        flash(f'Password has to be at least {PASSWORD_MIN_LEN} symbols long.', 'is-danger')
        return  redirect(url_for('auth.register'))
    elif not username:
        flash('Username cannot be empty.', 'is-danger')
        return redirect(url_for('auth.register'))

    #create new user
    new_user = User(username=username, password=generate_password_hash(password))

    #add new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash("User registered successfully.",'info')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for('main.index'))
