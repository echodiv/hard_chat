import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##### Flask-Mail #####
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT =  int(os.environ.get('') or 587)
    MAIL_USE_TLS =  os.environ.get('MAIL_USE_TLS') is not None 
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    ADMINS=['exzmple@mail.com']

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
