"""
Defines the blueprint for the authentication
"""
from flask import Blueprint
from flask_restful import Api

from app.resources import UserResource

BLUEPRINT_PREFIX = '/auth'
AUTH_BLUEPRINT = Blueprint("auth", __name__)


Api(AUTH_BLUEPRINT).add_resource(
    UserResource, '{}/user'.format(BLUEPRINT_PREFIX)
)
