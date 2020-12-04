import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    ''' Production config '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'

    ##### HardChat #####
    POST_PER_PAGE = 3
    LANGUAGES = ['en', 'ru']

    ##### Flask-Mail #####
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT =  int(os.environ.get('') or 587)
    MAIL_USE_TLS =  os.environ.get('MAIL_USE_TLS') is not None 
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    ADMINS=['exzmple@mail.com']
    
    # Elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    ##### SQLAlchemy #####
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

class TestConfig:
    ''' Test config '''
    TESTING = True
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
          'sqlite:///' + os.path.join(basedir, 'app.db')
