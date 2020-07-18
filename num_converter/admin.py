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
        flash("Šis puslapis prieinamas sistemos administratoriui", 'alert-error')
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
        flash("Šis puslapis prieinamas sistemos administratoriui", 'alert-error')
        return redirect(url_for('main.index'))


    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"Vartotojas {username} neegzistuoja.", 'alert-error')
    elif len(password) < PASSWORD_MIN_LEN:
        flash(f"Slaptažodis privalo būti bent {PASSWORD_MIN_LEN} symbolių ilgio.", 'alert-info')
    else:
        user.password = generate_password_hash(password)
        db.session.commit()

        flash(f"Vartotojo '{username}' slaptažodis buvo sėkmingai pakeistas.", 'alert-success')

    return redirect(url_for('admin.admin'))

@adm.route('/admin/delete', methods=['POST'])
@login_required
def admin_delete_post():
    if current_user.typee != 1:
        flash("Tik administratorius gali naudotis šia funkcija", 'alert-error')
        return redirect(url_for('main.index'))


    username = request.form.get('username')

    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"Vartoojas {username} neegzistuoja.", 'alert-error')
    elif username == 'admin':
        flash(f"Admnistratoriaus vartotojo ištrinti negalima!", 'alert-info')
    else:
        db.session.delete(user)
        db.session.commit()

        flash(f"Vartotojas '{username}' ištrintas sėkmingai.", 'alert-success')

    return redirect(url_for('admin.admin'))
