from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import click
from forms import NewNoteForm, EditNoteForm, DeleteNoteForm
from flask.helpers import flash, url_for
from werkzeug import abort, redirect
from flask.templating import render_template
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.secret_key = 'secret string'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    phone = db.Column(db.String(20), unique=True)
    # 不会作为字段存入数据库，快捷查询
    articles = db.relationship('Article')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))


@app.shell_context_processor
def extend_shell_context():
    """注册shell上下文处理函数
    Returns:
        [type] -- [description]
    """
    return {'db': db, 'Note': Note, 'Author': Author, 'Article': Article}


@app.route('/')
def index():
    notes = Note.query.all()
    form = DeleteNoteForm()
    return render_template('index.html', notes=notes, form=form)


@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    form = EditNoteForm()
    note = Note.query.get(id)
    if form.validate_on_submit():
        body = form.body.data
        note.body = body
        db.session.commit()
        flash('Your note is updated')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html', form=form)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted')
    else:
        abort(400)
    return redirect(url_for('index'))


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create all tables after drop all tables.')
def initdb(drop):
    """flask initdb [options]
    options:
    --drop drop all tables in database
    """
    if drop:
        click.confirm(
            "This operation will delete the database, do you want to continue?", abort=True)
        db.drop_all()
        click.echo('Drop tables')
    db.create_all()
    click.echo('Initialized database')
