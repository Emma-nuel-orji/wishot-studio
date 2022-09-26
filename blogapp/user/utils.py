from flask_mail import Message
from blogapp import mail
from flask import render_template, current_app
from threading import Thread
import os
import secrets
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_exe = os.path.splitext(form_picture.filename)
    fn_picture = random_hex + f_exe
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', fn_picture)
    output_size = (110, 110)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return fn_picture


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_token()
    send_email('[Wishot Studio] Reset Your Password', sender='wishotstudio@gmail.com', recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

