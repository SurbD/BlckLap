import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('BLCKLAP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'site.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # app.config['MAIL_DEFAULT_SENDER'] = "noreply@blcklap.com"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    BLCKLAP_MAIL_SUBJECT_PREFIX = '[BlckLap]'
    BLCKLAP_MAIL_SENDER = 'BlckLap Admin <noreply@blcklap.com>'