"""
Defines the blueprint for the authentication
"""
from flask import Blueprint
from flask_restful import Api


from resources import (
    UserResource, UserLoginResource, UserLogoutResource, ConfirmEmailResource,
    ChangePasswordResource, ResetPasswordResource, VerifyTokenResource, TokenRefreshResource,
    AuthorizeDeviceResource, UserListResource, SpecificUserResource
)


BLUEPRINT_PREFIX = '/auth'
AUTH_BLUEPRINT = Blueprint("auth", __name__)

api = Api(AUTH_BLUEPRINT)

# --------------------
# Path to client user
# --------------------
api.add_resource(UserResource, '{}/user'.format(BLUEPRINT_PREFIX))
api.add_resource(UserLoginResource, '{}/login'.format(BLUEPRINT_PREFIX))
api.add_resource(UserLogoutResource, '{}/logout'.format(BLUEPRINT_PREFIX))
api.add_resource(ConfirmEmailResource, '{}/confirm-email'.format(BLUEPRINT_PREFIX))
api.add_resource(ChangePasswordResource,'{}/change-password'.format(BLUEPRINT_PREFIX))
api.add_resource(ResetPasswordResource, '{}/reset-password'.format(BLUEPRINT_PREFIX))
api.add_resource(VerifyTokenResource, '{}/verify'.format(BLUEPRINT_PREFIX))
api.add_resource(TokenRefreshResource, '{}/refresh'.format(BLUEPRINT_PREFIX))
api.add_resource(AuthorizeDeviceResource, '{}/authorize-device'.format(BLUEPRINT_PREFIX))
        
# --------------------
# Path of admin user
# --------------------
api.add_resource(UserListResource, '{}/users'.format(BLUEPRINT_PREFIX))
api.add_resource(SpecificUserResource, '{}/user/<int:user_id>'.format(BLUEPRINT_PREFIX))
