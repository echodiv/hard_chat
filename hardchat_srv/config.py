import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Development config"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "A SECRET KEY"

    #  HardChat #####
    POST_PER_PAGE = int(os.environ.get("POST_PER_PAGE") or 3)
    MSG_PER_PAGE = int(os.environ.get("MSG_PER_PAGE") or 10)
    LANGUAGES = ["en", "ru"]

    #  Elasticsearch
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")

    #  SQLAlchemy #####
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")


class TestConfig:
    """Test config"""

    TESTING = True
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
