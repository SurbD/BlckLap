from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_required, current_user

from flaskapp import db
from flaskapp.models import User
from flaskapp.users.forms import UpdateAccountForm
from flaskapp.utils import send_email, save_picture, delete_old_picture

users = Blueprint('users', __name__)


@users.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            old_picture = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            delete_old_picture(old_picture)
        current_user.username = form.username.data
        db.session.commit()

        if form.email.data != current_user.email:
            token = current_user.get_email_token(email=form.email.data)
            send_email(form.email.data, 'Email Update',\
                        'email/update_email', user=current_user, token=token)
            flash('A confirmation email has been sent to you by email.', 'success')
            return redirect(url_for('users.account'))
        # current_user.email = form.email.data

        flash('Your account has been successfully updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', form=form, title='Account', image_file=image_file)




@users.route('/confirm_email/<token>')
@login_required
def confirm_email(token):
    data = current_user.confirm_email_token(token)
    print(data)

    if data:
        user = User.query.get(data.get('user_id'))
        email = data.get('email')
        user.email = email

        db.session.add(user)
        db.session.commit()
        flash('You have updated your email, Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired', 'danger')
    return redirect(url_for('main.home'))


@users.route('/user/<int:user_id>/')
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', title=user.username, user=user)