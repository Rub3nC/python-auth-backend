from flask_restful import Api
# Test function
from .controller import (
    Test, User, UserLogin, UserLogout, ConfirmEmail, ChangePassword, ResetPassword,
    VerifyToken, TokenRefresh, AuthorizeDevice, UserList, SpecificUSer
)

class RoutesAuth:
    version_base_dir = "/v1"
    auth_base_dir = version_base_dir+"/auth"

    @classmethod
    def add_route(cls, blueprint: object) -> None:
        api = Api(blueprint)
        api.add_resource(Test, "{}/<string:name>".format(cls.auth_base_dir))
        
        # --------------------
        # Path to client user
        # --------------------
        api.add_resource(User, '{}/user'.format(cls.auth_base_dir))
        api.add_resource(UserLogin, '{}/login'.format(cls.auth_base_dir))
        api.add_resource(UserLogout, '{}/logout'.format(cls.auth_base_dir))
        api.add_resource(ConfirmEmail, '{}/confirm-email'.format(cls.auth_base_dir))
        api.add_resource(ChangePassword,'{}/change-password'.format(cls.auth_base_dir))
        api.add_resource(ResetPassword, '{}/reset-password'.format(cls.auth_base_dir))
        api.add_resource(VerifyToken, '{}/verify'.format(cls.auth_base_dir))
        api.add_resource(TokenRefresh, '{}/refresh'.format(cls.auth_base_dir))
        api.add_resource(AuthorizeDevice, '{}/authorize-device'.format(cls.auth_base_dir))
        
        # --------------------
        # Path of admin user
        # --------------------
        api.add_resource(UserList, '{}/users'.format(cls.auth_base_dir))
        api.add_resource(SpecificUSer, '{}/user/<int:user_id>'.format(cls.auth_base_dir))