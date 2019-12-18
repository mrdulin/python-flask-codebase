from flask import Flask
from flask_mail import Mail, Message
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('novaline', os.getenv('MAIL_DEFAULT_SENDER'))
)
print(app.config)

mail = Mail(app)


def sendgrid_send_mail():
    message = Mail(
        from_email=os.getenv('MAIL_DEFAULT_SENDER'),
        to_emails='novaline.dulin@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))


def send_mail(subject, to, body):
    with app.app_context():
        message = Message(subject='IMAP服务目前有什么功能限制?', recipients=[
            'novaline.dulin@gmail.com'], body='IMAP服务目前有什么功能限制？')
        mail.send(message)


# sendgrid_send_mail()
