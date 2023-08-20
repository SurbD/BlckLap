import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin
from flaskapp import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    def get_token(self, expiration=600):
        token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return token
    
    @staticmethod
    def confirm_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        if not (user_id := data.get('user_id')):
            return None
        return User.query.get(user_id)

    # <!-- For Email Token -->

    def get_email_token(self, expiration=600, **kwargs): # new_email=None
        payload = {
            "user_id": self.id, 
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
        }
        payload.update(kwargs)
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return token
    
    @staticmethod
    def confirm_email_token(token):
        try:
            data = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )
        except:
            return True
        
        if not (user_id := data.get('user_id')) and not(data.get('email')):
            return None
        return data
    # <!-- End Email Token -->

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"