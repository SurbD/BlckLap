from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user

from flaskapp.models import User

main = Blueprint('main', __name__)

    
@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        # users = User.query.order_by(User.id.desc()).all()
        page = request.args.get('page', 1, type=int)
        users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=3)
        return render_template('home.html', users=users)
    else:
        return render_template('index.html')
    

@main.route('/settings')
def settings():
    return render_template('settings.html')