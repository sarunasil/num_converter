import os

from os.path import join, splitext, exists, basename

from flask import Blueprint, render_template, url_for, request, redirect, current_app, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from .utils import convert, read_txt, read_excel, read_word, write_txt, write_excel, write_word

ALLOWED_EXTENSIONS = {'txt', 'xls', 'xlsx', 'docx' }
EXPORT_FORMATS = {'txt', 'xlsx', 'docx'}

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
    return render_template('converter.html', export_formats=EXPORT_FORMATS, allowed_extensions=ALLOWED_EXTENSIONS, selected_format='txt')

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS

@main.route('/converter', methods=["POST"])
def converter_post():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('main.converter'))
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('main.converter'))
    export_format = request.form['export_format']
    if export_format not in EXPORT_FORMATS:
        flash('Forbidden export format')
        return redirect(url_for('main.converter'))


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            if filename.endswith('txt'):
                content = read_txt(filepath)
            elif filename.endswith('xls') or filename.endswith('xlsx'):
                content = read_excel(filepath)
            elif filename.endswith('docx'):
                content = read_word(filepath)

            converted = convert(content)
        except:
            converted = set()
            flash("Failed to read or convert the file. Try again")


        ofilepath = f"{splitext(filepath)[0]}_converted.{export_format}"
        try:
            if export_format == 'txt':
                write_txt(ofilepath, converted)
            elif export_format == 'xlsx' or export_format == 'xls':
                write_excel(ofilepath, converted)
            elif export_format == 'docx':
                write_word(ofilepath, converted)
        except:
            flash("Failed to save converted file. Try again")

        #delete prev file
        os.remove(filepath)

        session['ofilepath'] = basename(ofilepath)

        return render_template('converter.html', export_formats=EXPORT_FORMATS, allowed_extensions=ALLOWED_EXTENSIONS, before_size=len(content), after_size=len(converted), selected_format=export_format)
    else:
        flash(f'Provide file of accepted format: {", ".join(ALLOWED_EXTENSIONS)}.' )

    return redirect(url_for('main.converter'))

@main.route('/download', methods=["POST"])
def download():

    if session['ofilepath']:
        uploads = join(os.getcwd(), current_app.config['UPLOAD_FOLDER'])

        if exists( join(uploads, session['ofilepath'])):
            return send_from_directory(directory=uploads, filename=session['ofilepath'], as_attachment=True)
        else:
            return "Error occurred. Seems the input file was not converted properly. Try again"

@main.route('/reset_form', methods=['POST'])
def reset():

    filelist = [ f for f in os.listdir(current_app.config['UPLOAD_FOLDER']) if not f.endswith(".gitignore") ]
    for f in filelist:
        os.remove(join(current_app.config['UPLOAD_FOLDER'], f))

    return redirect(url_for('main.converter'))


@main.route('/sveplinimas', methods=['GET'])
def sveplinimas():
    return render_template('sveplinimas.html')