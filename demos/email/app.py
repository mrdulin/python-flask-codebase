from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('novaline', os.getenv('MAIL_DEFAULT_SENDER'))
)
print(app.config)

mail = Mail(app)

# def send_mail(subject, to, body):
with app.app_context():
    message = Message(subject='Hello, world!', recipients=[
        '365715693@qq.com'], body='IMAP服务目前有什么功能限制？')
    mail.send(message)
