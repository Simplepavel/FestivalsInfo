import secrets
import os
from Festival.database.model import User
from flask_mail import Message
from flask import url_for
from Festival import mail


def save_picture(save_picture):
    new_name = secrets.token_hex(8)
    _, f_ext = os.path.splitext(save_picture.filename)
    new_name += f_ext
    save_path = "Festival/static/image_profile/" + new_name
    save_picture.save(save_path)
    return new_name


def send_mail(user: User):
    msg = Message("Смена пароля", recipients=[user.email], sender="")
    msg.body = f'''Для смены пароля перейдите по данному адресу:
    {url_for('reset_password', token = user.get_own_verify_token(), _external = True)}
    '''
    mail.send(msg)
