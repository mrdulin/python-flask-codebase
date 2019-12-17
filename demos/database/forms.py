from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditNoteForm(NewNoteForm):
    submit = SubmitField('Update')


class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')
