from flask import Flask, request, redirect, session
from flask.helpers import make_response, url_for
from werkzeug.exceptions import abort
import json
from flask.json import jsonify
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret thing')


@app.route('/hello')
def hello():
    # name = request.args['name']
    # better
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Flask')
        response = '<h1>Hello, {name}</h1>'.format(name=name)
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
    return response


@app.route('/goback/<int:year>')
def go_back(year):
    return f'<p>Welcome to {2019 - year}</p>'


colors = ['blue', 'white', 'red']
@app.route(f'/color/<any({str(colors)[1:-1]}):color>')
def three_colors(color):
    return f'<p>color: {color}</p>'


@app.route('/myredirect')
def my_redirect():
    return '', 302, {'Location': 'https://github.com'}


@app.route('/flask_redirect')
def flask_redirect():
    return redirect('https://github.com')


@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


@app.route('/404')
def not_found():
    abort(404)


@app.route('/foo')
def foo():
    response = make_response('Hello world!')
    response.mimetype = 'text/plain'
    return response


@app.route('/api/foo')
def api_foo():
    data = {
        'name': 'mrdulin',
        'gender': 'male'
    }
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response
    # better
    return jsonify(data)


@app.route('/api/bar')
def api_bar():
    return jsonify(message='Error!'), 500


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'
