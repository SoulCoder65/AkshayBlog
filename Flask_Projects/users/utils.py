import os

from PIL import Image
from flask_mail import Message
from flask import url_for, current_app
from Flask_Projects import mail
import random
import string

def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
generate_key(10)
def save_picture(form_picture):
    random_hex = generate_key(10)
    _, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.root_path, 'static/profilepic', picture_fn)
    output_size = (125, 125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Request from Soul Blog',
                sender='dumy@gmail.com',
                recipients=[user.email]
                )
    msg.body=f'''To reset Password,click on the link below:
    {url_for('users.reset_token',token=token,_external=True)}
    
    Thanks You From Soul Blog and Team. Have a Nice Day!!
     '''
    mail.send(msg)
