from flask_marshmallow import Marshmallow

ma = Marshmallow()

from .auth import UserRegistrationSchema, UserSchema, UserLoginSchema, UserUpdateSchema