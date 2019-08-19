from flask import Flask, Blueprint
from .config import config_by_name

from app import routes


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    for blueprint in vars(routes).values():
        if isinstance(blueprint, Blueprint):
            app.register_blueprint(blueprint, url_prefix='/v1')

    return app