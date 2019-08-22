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
        errors = []
        if PasswordStats(value).strength() < password_validators["strength"]:
            errors.append({'strength': 'The password is very simple.'})

        if PasswordStats(value).length < password_validators["length"]:
            errors.append({'length': 'The password must be at least {} characters.'.
                format(password_validators["length"])})

        if PasswordStats(value).numbers < password_validators["numbers"]:
            errors.append({'numbers': 'The password must have at least {} numbers.'.
                format(password_validators["numbers"])})

        if PasswordStats(value).letters_uppercase < password_validators["uppercase"]:
            errors.append({'uppercase': 'The password must have at least {} uppercase letters.'.
                format(password_validators["uppercase"])})

        if PasswordStats(value).special_characters < password_validators["special"]:
            errors.append({'special': 'The password must have be at least {} special characters.'.
                format(password_validators["special"])})

        if errors:
            raise ValidationError(errors)