from flask import Flask, session
from forms import LoginForm, UploadForm
from flask.templating import render_template
from flask.helpers import flash, send_from_directory, url_for
from werkzeug import redirect
import os
import uuid

app = Flask(__name__)
app.secret_key = 'secret string'
# 请求报文最大长度限制3M
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')


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


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded')
def show_images():
    filename = session['filenames'][0]
    return render_template('uploaded.html', filename=filename)
