from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes  # for testing from console

    # Create tables from the models; only possible on server run
    # as db out of function scope (necessary for access from other
    # modules
        #db.create_all()

    return app
