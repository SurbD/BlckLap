from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from flaskapp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # <!-- Add routes and custom error pages here  --> 
    from flaskapp.users.routes import users
    from flaskapp.auth.routes import auth
    from flaskapp.main.routes import main
    from flaskapp.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app