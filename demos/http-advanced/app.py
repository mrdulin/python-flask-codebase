from flask import Flask, request
from flask.helpers import url_for
from werkzeug import redirect
from urllib.parse import urljoin, urlparse

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello, world'


@app.route('/foo')
def foo():
    return '<h1>Foo page<a href="{href}">Do something</a></h1>'.format(href=url_for('do_something', next=request.full_path))


@app.route('/bar')
def bar():
    return '<h1>Bar page<a href="{href}">Do something</a></h1>'.format(href=url_for('do_something', next=request.full_path))


@app.route('/do_something')
def do_something():
    """
    1. 使用HTTP referrer重定向到上一个（来源）页面, referrer的值可能为""，因此使用url_for('hello')作为回退方案
    2. 查询参数
    Returns:
        [type] -- [description]
    """
    return redirect_back()


def is_safe_url(target):
    """验证重定向url，防范开放重定向漏洞

    Arguments:
        target {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
