import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##### настройка Flask-Mail #####
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    ADMINS = ['your-email@example.com']
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
