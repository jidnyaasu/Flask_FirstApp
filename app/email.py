from threading import Thread

from flask import render_template
from flask_mail import Message
from social_app import app


def send_async_email(msg):
    with app.app_context():
        app.mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config["MAIL_SUBJECT_PREFIX"] + " " + subject,
                  sender=app.config["SOCIAL_APP_MAIL_SENDER"], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()
    return thr
