from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

from . import db
from .models import User

adm = Blueprint('admin', __name__)

@adm.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.typee != 1:
        return redirect(url_for('main.index'))


    users = User.query.all()

    usernames = []
    for user in users:
        usernames.append(user.username)

    return render_template('admin.html', usernames=usernames)

