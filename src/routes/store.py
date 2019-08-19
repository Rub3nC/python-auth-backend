"""
Defines the blueprint for the store resource
"""
from flask import Blueprint
from flask_restful import Api

from resources import StoreResource, StoreItemsResource


BLUEPRINT_PREFIX = '/store'
STORE_BLUEPRINT = Blueprint('store', __name__)

api = Api(STORE_BLUEPRINT)

api.add_resource(StoreResource, '{}/'.format(BLUEPRINT_PREFIX))
api.add_resource(StoreItemsResource, '{}/items'.format(BLUEPRINT_PREFIX))
