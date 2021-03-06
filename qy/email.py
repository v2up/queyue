from threading import Thread

from flask import current_app, render_template
from flask.ext.mail import Message

from . import mail

def send_confirm_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['QY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                sender=app.config['QY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_confirm_mail_async, args=[app, msg])
    thr.start()
    return thr

def send_confirm_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)
