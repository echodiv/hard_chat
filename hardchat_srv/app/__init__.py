import logging
from datetime import datetime

from elasticsearch import Elasticsearch
from flask import Flask, current_app, g, request
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app.main.forms import SearchForm
from app.urls import register_error_handlers, register_routers
from config import BaseConfig

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


def set_middlewares(app: Flask, db: SQLAlchemy) -> None:
    @app.before_request
    def user_detector():
        if current_user.is_authenticated:
            current_user.last_visit_time = datetime.utcnow()
            db.session.commit()
            g.search_form = SearchForm()
        g.locale = str(get_locale())


def create_app(config_class=BaseConfig) -> Flask:
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

    app.logger.setLevel(logging.INFO)
    app.logger.info("🚀 Microblog startup")

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])


from app import models
