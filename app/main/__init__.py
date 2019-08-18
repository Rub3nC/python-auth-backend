from flask import Flask, Blueprint
from .config import config_by_name
from .route import RoutesAuth


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Route group for api_auth
    api_auth_bp = Blueprint('api_auth', __name__)
    RoutesAuth.add_route(app)
    app.register_blueprint(api_auth_bp)
    
    return app