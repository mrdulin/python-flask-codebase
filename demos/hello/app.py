from flask import Flask
import click

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'


@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, {name}</h1>'.format(name=name)


# 创建自定义命令
@app.cli.command()
def hello():
    """
    使用方式：flask hello
    """
    click.echo('Hello, Human!')
