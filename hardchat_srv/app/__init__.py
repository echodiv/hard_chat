import logging
import os
from datetime import datetime

from logging.handlers import RotatingFileHandler, SMTPHandler

from config import BaseConfig
from elasticsearch import Elasticsearch
from flask import Flask, current_app, request, g
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app.main.forms import SearchForm
from app.urls import register_routers, register_error_handlers

# flask modules
babel = Babel()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
login = LoginManager()
# settings for login manager
login.login_view = "auth.login"
login.login_message = "Please log in to access this page"


def set_middlewares(app: Flask, db) -> None:
    @app.before_request
    def user_detector():
        if current_user.is_authenticated:
            current_user.last_visit_time = datetime.utcnow()
            db.session.commit()
            g.search_form = SearchForm()
        g.locale = str(get_locale())


def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    register_routers(app)
    register_error_handlers(app)
    set_middlewares(app, db)

    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr="no-reply@" + app.config["MAIL_SERVER"],
                toaddrs=app.config["ADMINS"],
                subject="Microblog Failure",
                credentials=auth,
                secure=secure,
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/HARDCHAT.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Microblog startup")

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])


from app import models
