from flask import Flask, session, request
from forms import LoginForm, UploadForm, MultipleUploadForm
from flask.templating import render_template
from flask.helpers import flash, send_from_directory, url_for
from werkzeug import redirect
import os
import uuid
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError


app = Flask(__name__)
app.secret_key = 'secret string'
# 请求报文最大长度限制3M
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSTION'] = ['jpg', 'png', 'gif', 'jpeg']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, {}!'.format(username))
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)


@app.route('/bootstrap')
def bootstrap():
    form = LoginForm()
    return render_template('bootstrap.html', form=form)


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.photo.data
        filename = random_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload Success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


def allowed_file(filename):
    return os.path.splitext(filename)[1][1:] in app.config['ALLOWED_EXTENSTION']


@app.route('/multiple_upload', methods=['GET', 'POST'])
def multiple_upload():
    form = MultipleUploadForm()
    if request.method == 'POST':
        filenames = []
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('csrf token error')
            return redirect(url_for('multiple_upload'))
        if 'photos' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multiple_upload'))
        for f in request.files.getlist('photos'):
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multiple_upload'))
        flash('upload success')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('multiple_upload.html', form=form)


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded')
def show_images():
    filenames = session['filenames']
    return render_template('uploaded.html', filenames=filenames)
