from flask import Flask, Blueprint
from flask_migrate import Migrate

import routes
from models import db
from schemas import ma
from .config import config_by_name
from .bcrypt import app_bcrypt


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    for blueprint in vars(routes).values():
        if isinstance(blueprint, Blueprint):
            app.register_blueprint(blueprint, url_prefix='/v1')

    db.init_app(app)
    app_bcrypt.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    return app