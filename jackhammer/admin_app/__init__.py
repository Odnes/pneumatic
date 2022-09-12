from flask import Flask
from ..instantiate_db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('jackhammer.config.default_config')

    db.init_app(app)

    with app.app_context():
        from . import routes  # for testing from console
 
    return app
