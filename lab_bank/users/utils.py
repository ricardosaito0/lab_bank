import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from lab_bank import mail
from flask import current_app

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pictures', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
    
def send_reset_email(user):
    
    token = user.get_reset_token()
    msg = Message('Requisição de alteração de senha', sender = 'reset.psswd0@gmail.com', recipients = [user.email])
    msg.body = f'Para alterar sua senha, acesse esse link: \n {url_for('users.reset_password', token = token, _external = True)} \n Se essa requisição não foi feita por você, ignore essa mensagem.'
    
    mail.send(msg)