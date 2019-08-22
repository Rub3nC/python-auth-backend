import os
from marshmallow import validates, ValidationError
from password_strength import PasswordPolicy, PasswordStats
from . import ma

from models import UserModel
from main.config import config_by_name
config = config_by_name[os.getenv('APP_ENV') or 'dev']

password_validators = config.AUTH_PASSWORD_VALIDATORS_PARAMETERS


class UserSchema(ma.Schema):
    class Meta:
        fields = (
        	'username',
        	'email',
        	'password',
        	'first_name',
        	'last_name',
        	'is_active'
        )
        
    @validates("password")
    def validate_password(self, value):
        if PasswordStats(value).strength() < password_validators["strength"]:
            raise ValidationError("The password is very weak")

        policy = PasswordPolicy.from_names(
            length=password_validators["length"],  
            uppercase=password_validators["uppercase"],
            numbers=password_validators["numbers"],
            special=password_validators["special"],
            nonletters=password_validators["nonletters"],
        )
        if policy.test(value):
            text_e = ''
            for p in policy.test(value):
                text_e += '{}, '.format(p)
            raise ValidationError("Password does not comply with {}".format(
            	text_e[0:len(text_e) - 2])
            )