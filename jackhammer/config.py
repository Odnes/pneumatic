from os import environ


class Config:

    # General
    SECRET_KEY = environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = \
        environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    ARTICLES_PER_PAGE = 3

    # Articles repository
    # Should replace ordinary github filepaths with their raw counterparts
    ARTICLES_REPO = environ.get("ARTICLES_REPO")
