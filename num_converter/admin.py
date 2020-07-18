from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from . import db
from .models import User
from .auth import PASSWORD_MIN_LEN

adm = Blueprint('admin', __name__)

@adm.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.typee != 1:
        flash("Only admin can access this page", 'is-danger')
        return redirect(url_for('main.index'))


    users = User.query.all()

    usernames = []
    for user in users:
        usernames.append(user.username)

    return render_template('admin.html', usernames=usernames)

@adm.route('/admin/save', methods=['POST'])
@login_required
def admin_save_post():
    if current_user.typee != 1:
        flash("Only admin can make such changes", 'is-danger')
        return redirect(url_for('main.index'))


    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"User {username} doesn't exist.", 'is-danger')
    elif len(password) < PASSWORD_MIN_LEN:
        flash(f"Password has to be atleast {PASSWORD_MIN_LEN} symbols long.")
    else:
        user.password = generate_password_hash(password)
        db.session.commit()

        flash(f"User '{username}' password changed successfully.")

    return redirect(url_for('admin.admin'))

@adm.route('/admin/delete', methods=['POST'])
@login_required
def admin_delete_post():
    if current_user.typee != 1:
        flash("Only admin can make such changes", 'is-danger')
        return redirect(url_for('main.index'))


    username = request.form.get('username')

    user = User.query.filter_by(username=username).first()
    if not user:
        pass
        # flash(f"User {username} doesn't exist.", 'is-danger')
    else:
        db.session.delete(user)
        db.session.commit()

        flash(f"User '{username}' deleted successfully.")

    return redirect(url_for('admin.admin'))