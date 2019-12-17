from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired, Length
from wtforms.fields.simple import BooleanField, FileField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'placeholder': 'Your name'}, validators=[
                           DataRequired()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=128, message='密码长度必须大于8个字符，小于128个字符')])

    remember = BooleanField(label='Remember me')
    submit = SubmitField(label='Log in')


class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[
                      FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField()
