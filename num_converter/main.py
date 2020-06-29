from os import remove, getcwd
from os.path import join, splitext, exists, basename

from flask import Blueprint, render_template, url_for, request, redirect, current_app, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from .utils import convert

ALLOWED_EXTENSIONS = {'txt', 'xls' }

main = Blueprint('main', __name__)

@main.route('/', defaults={'path': ''}, methods=["POST","GET"])
@main.route('/<path:path>', methods=["POST", "GET"])
def default(path):
    return redirect(url_for('main.converter'))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/converter')
def converter():
    return render_template('converter.html')

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS

def read_txt(filepath):
    lines = []
    with open(filepath, 'r') as file1:
        lines = file1.readlines()

    return lines

@main.route('/converter', methods=["POST"])
def converter_post():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('main.converter'))
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('main.converter'))


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        content=""
        if filename.endswith('txt'):
            content = read_txt(filepath)
        elif filename.endswith('xls'):
            pass

        converted = convert(content)

        ofilepath = f"{splitext(filepath)[0]}_converted.txt"
        with open(ofilepath, 'w') as ofile:
            ofile.writelines(converted)

        #delete prev file
        remove(filepath)

        session['ofilepath'] = basename(ofilepath)

        return render_template('converter.html', before_size=len(content), after_size=len(converted))

    return redirect(url_for('main.converter'))

@main.route('/download', methods=["POST"])
def download():

    if session['ofilepath']:
        uploads = join(getcwd(), current_app.config['UPLOAD_FOLDER'])

        if exists( join(uploads, session['ofilepath'])):
            return send_from_directory(directory=uploads, filename=session['ofilepath'])
        else:
            return "Error occurred. Seems the input file was not converted properly. Try again"
