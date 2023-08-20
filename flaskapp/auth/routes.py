from flask import Blueprint, redirect, url_for, render_template, request, flash, session
from flask_login import login_user, login_required, current_user, logout_user

from flaskapp import db, bcrypt
from flaskapp.auth.forms import (LoginForm, RegistrationForm, RequestResetForm,
                                  ResetPasswordForm, ChangePasswordForm)
from flaskapp.models import User
from flaskapp.utils import send_email

auth = Blueprint('auth', __name__)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
    
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('unconfirmed.html')

@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # for login_query with login_required
            if '/logout' == next_page: # Checks if next is directing user to logout so it returns back to home
                next_page = None
                
            # flash("You're Logged In!", 'success')
            session['email'] = None
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger') # Remember to edit Flash message and write good comment for this project
            session['email'] = form.email.data
            return redirect(url_for('auth.login')) # To avoid Form resubmission
    elif request.method == 'GET':
        email = session.get('email')
        form.email.data = email if email else ''
    return render_template('login.html', form=form, title='Login')


@auth.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        token = user.get_token()
        send_email(user.email, 'Confirm Your Account', 
                   'email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.', 'success')
        # flash('Your account has been created Successfully, You can now Login!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, title='Register')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('You have been logged out!', 'success')
    return redirect(url_for('main.home'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    
    user = current_user.confirm_token(token)
    if user:
        user.confirmed = True 
        db.session.add(user)
        db.session.commit()
        flash('Your have confirmed your account, Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired', 'danger')
    return redirect(url_for('main.home'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.get_token()
    # print(current_user)
    send_email(current_user.email, 'Confirm Your Account', 
                   'email/confirm', user=current_user, token=token)
    flash('A confirmation email has been sent to you by email.', 'success')
    return redirect(url_for('main.home'))

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_token()
        send_email(user.email, 'Password Reset', \
                   'email/password_reset', user=user, token=token)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.confirm_token(token)
    if not user:
        flash('That is an invalid or expired token', 'danger')
        return redirect(url_for('auth.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your Password has been updated!, You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            # db.session.add(current_user)
            db.session.commit()
            flash('Your Password has been updated!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid Password. Check Password and try again', 'danger')

    return render_template('change_password.html', form=form, title='Change Password')