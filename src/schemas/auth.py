import os
import re
from marshmallow import fields,validate, validates, ValidationError, pre_load
from password_strength import PasswordPolicy, PasswordStats
from . import ma

from models import UserModel
from main.config import config_by_name
config = config_by_name[os.getenv('APP_ENV') or 'dev']

password_validators = config.AUTH_PASSWORD_VALIDATORS_PARAMETERS
account_authentication_method = config.ACCOUNT_AUTHENTICATION_METHOD


class UserRegistrationSchema(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()
        
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


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("confirmation", "password_hash", "created_at", "update_at")


class UserLoginSchema(ma.Schema):
    username = fields.String()
    email = fields.Email()
    password = fields.String(required=True)

    @pre_load
    def _pre_load(self, data):
        if account_authentication_method == "username" and not "username" in data:
            raise ValidationError({"username": ["Missing data for required field."]})
        
        if account_authentication_method == "email" and not "email" in data:
            raise ValidationError({"email": ["Missing data for required field."]})

        if account_authentication_method == "username_email":
            if not "email" in data and not "username" in data:
                raise ValidationError({"username or email": ["Missing data for required field."]})
            
        return data

class UserUpdateSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    is_active = fields.Boolean(required=True)