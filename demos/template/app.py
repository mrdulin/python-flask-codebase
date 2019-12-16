from flask import Flask
from flask.templating import render_template
import datetime
from jinja2 import Markup
from flask.helpers import flash, url_for
from werkzeug import redirect

app = Flask(__name__)
app.secret_key = 'secret thing'

print('app.jinja_env.globals: ', app.jinja_env.globals, '\n')
print('app.jinja_env.filters: ', app.jinja_env.filters, '\n')
print('app.jinja_env.tests: ', app.jinja_env.tests)

# 自定义上下文
app.context_processor(lambda: {'foo': 'I am foo.'})
@app.context_processor
def inject_bar():
    return {'bar': 'I am bar.'}

# 自定义全局函数


def current_time():
    return datetime.datetime.now()


app.add_template_global(current_time)
@app.template_global()
def baz():
    return 'I am baz.'

# 自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup('&#9385;')


@app.route('/')
def home():
    # 标记为安全的文本
    text = Markup('<h1>Hello, Jinjia2 </h1>')
    return render_template('index.html', text=text)


@app.route('/user_profile')
def user_profile():
    user = {
        "username": 'mrdulin',
        'bio': "keep coding"
    }
    return render_template('user_profile.html', user=user)


@app.route('/test_flash')
def just_flash():
    flash('I am flash.')
    return redirect(url_for('home'))


@app.errorhandler(code_or_exception=404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
