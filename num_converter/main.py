from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''}, methods=["POST","GET"])
@main.route('/<path:path>', methods=["POST", "GET"])
def default(path):
    return redirect(url_for('conv.converter'))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)


@main.route('/sveplinimas', methods=['GET'])
@login_required
def sveplinimas():
    return render_template('sveplinimas.html')
