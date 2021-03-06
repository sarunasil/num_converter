import os

from os.path import join, splitext, exists, basename

from flask import Blueprint, render_template, url_for, request, redirect, current_app, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required

from .utils import convert, read_txt, read_excel, read_word, write_txt, write_excel, write_word

ALLOWED_EXTENSIONS = {'txt', 'xls', 'xlsx', 'docx' }
EXPORT_FORMATS = {'txt', 'xlsx', 'docx'}

conv = Blueprint('conv', __name__)

@conv.route('/converter')
@login_required
def converter():
    return render_template('converter.html', export_formats=EXPORT_FORMATS, allowed_extensions=ALLOWED_EXTENSIONS, selected_format='txt')

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS

@conv.route('/converter', methods=["POST"])
@login_required
def converter_post():
    if 'file' not in request.files:
        flash('Nerastas joks failas', 'alert-error')
        return redirect(url_for('conv.converter'))
    file = request.files['file']
    if file.filename == '':
        flash('Nepasirinktas joks failas', 'alert-error')
        return redirect(url_for('conv.converter'))
    export_format = request.form['export_format']
    if export_format not in EXPORT_FORMATS:
        flash('Export format not supported', 'alert-info')
        return redirect(url_for('conv.converter'))


    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        filepath = join(current_app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(filepath)

            if filename.endswith('txt'):
                content = read_txt(filepath)
            elif filename.endswith('xls') or filename.endswith('xlsx'):
                content = read_excel(filepath)
            elif filename.endswith('docx'):
                content = read_word(filepath)

            converted = convert(content)

            ofilepath = splitext(filepath)[0] +"_converted." + export_format
            try:
                if export_format == 'txt':
                    write_txt(ofilepath, converted)
                elif export_format == 'xlsx' or export_format == 'xls':
                    write_excel(ofilepath, converted)
                elif export_format == 'docx':
                    write_word(ofilepath, converted)
            except:
                flash("Nepavyko išsaugoti konvertuoto failo. Pabandykite dar kartą.", 'alert-info')

            #delete prev file
            os.remove(filepath)

        except Exception as e:
            content = set()
            converted = set()
            flash("Įvyko klaida, nebuvo įmanoma perskaityti įkelto failo. Pabandykite dar kartą.", 'alert-info')


        session['ofilepath'] = basename(ofilepath)

        return render_template('converter.html', export_formats=EXPORT_FORMATS, allowed_extensions=ALLOWED_EXTENSIONS, before_size=len(content), after_size=len(converted), selected_format=export_format)
    else:
        flash("Priimami failų formatai: " + {", ".join(ALLOWED_EXTENSIONS)} + ".", 'alert-info')

    return redirect(url_for('conv.converter'))

@conv.route('/download', methods=["POST"])
@login_required
def download():

    if session['ofilepath']:
        uploads = current_app.config['UPLOAD_FOLDER']

        if exists( join(uploads, session['ofilepath'])):
            return send_from_directory(directory=uploads, filename=session['ofilepath'], as_attachment=True)
        else:
            return "Įvyko klaida. Jūsų failas nebuvo sėkmingai konvertuotas. Pabandykite dar kartą."

@conv.route('/reset_form', methods=['POST'])
@login_required
def reset():

    filelist = [ f for f in os.listdir(current_app.config['UPLOAD_FOLDER']) if not f.endswith(".gitignore") ]
    for f in filelist:
        os.remove(join(current_app.config['UPLOAD_FOLDER'], f))

    return redirect(url_for('conv.converter'))
