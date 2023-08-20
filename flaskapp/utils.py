from PIL import Image
from flask import render_template, current_app
from flask_mail import Message

import os
import secrets
from threading import Thread

from flaskapp import mail

# <!-- Utility Functions

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

def delete_old_picture(pic_filename):
    # pic_path = os.path.join(current_app.root_path, 'static/profile_pic', pic_filename)
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics')
    pic_path_dir = os.listdir(pic_path)
    
    if (pic_filename in pic_path_dir) and pic_filename != 'default.jpg':
        try:
            os.remove(os.path.join(pic_path, pic_filename))
        except OSError:
            pass

def send_async_email(app, msg): 
    with app.app_context(): 
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['BLCKLAP_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['BLCKLAP_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    # try:
    #     mail.send(msg)
    # except:
    #     abort(500)
        
# ... End of Utility Functions -->