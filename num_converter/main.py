from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''}, methods=["POST","GET"])
@main.route('/<path:path>', methods=["POST", "GET"])
def default(path):
    return redirect(url_for('conv.converter'))

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('conv.converter'))
    else:
        return render_template('index.html')


@main.route('/sveplinimas', methods=['GET'])
@login_required
def sveplinimas():
    return render_template('sveplinimas.html')
