from flask_restful import Api
# Test function
from .controller import Test

class RoutesAuth:
    version_base_dir = "/v1"
    auth_base_dir = version_base_dir+"/auth"

    @classmethod
    def add_route(cls, blueprint: object) -> None:
        api = Api(blueprint)
        api.add_resource(Test, "{}/<string:name>".format(cls.auth_base_dir))
        
        '''
        These are the project initial routes
        
        --------------------
        Path to client user
        --------------------
        api.add_resource(cls.auth_base_dir+'/user', 'user', hello_world)
        api.add_resource(cls.auth_base_dir+'/login', 'login', hello_world)
        api.add_resource(cls.auth_base_dir+'/logout', 'logout', hello_world)
        api.add_resource(cls.auth_base_dir+'/confirm-email', 'confirm_email', hello_world)
        api.add_resource(cls.auth_base_dir+'/change-password', 'change_password', hello_world)
        api.add_resource(cls.auth_base_dir+'/reset-password', 'reset_password', hello_world)
        api.add_resource(cls.auth_base_dir+'/verify', 'verify', hello_world)
        api.add_resource(cls.auth_base_dir+'/refresh', 'refresh', hello_world)
        api.add_resource(cls.auth_base_dir+'/authorize-device', 'authorize_device', hello_world)
        
        --------------------
        Path of admin user
        --------------------
        api.add_resource(cls.auth_base_dir+'/users', 'users_list', hello_world)
        api.add_resource(cls.auth_base_dir+'/user/<int:user_id>', 'specific_user', hello_world)
        '''