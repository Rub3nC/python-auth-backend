from requests import Response
from flask import request, url_for
from functools import wraps
from main.bcrypt import app_bcrypt

import os
import bcrypt
import jwt
from time import time
from datetime import datetime, timedelta
from models import UserModel, EmailConfirmationModel, BlacklistTokenModel
#from libs import Mailgun
from libs import SendMail
from .exceptions import InvalidTokenError, TokenExpiredError

from main.config import config_by_name
config = config_by_name[os.getenv('APP_ENV') or 'dev']


INVALID_TOKEN = "Token is invalid or missing."
TOKEN_EXPIRED = "Authentication token has expired."


class UserService:
    """ The service for the user model """

    @staticmethod
    def get_by_id(user_id: int) -> "UserModel":
        """ Query a user by id """
        return UserModel.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_username(username: str) -> "UserModel":
        """ Query a user by username """
        return UserModel.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email: str) -> "UserModel":
        """ Query a user by email """
        return UserModel.query.filter_by(email=email).first()

    @staticmethod
    def get_all() -> "UserModel":
        """ Query all users """
        return UserModel.query.all()

    @classmethod
    def validate_credentials(cls, username:str, password:str) -> bool:
        user = cls.get_by_username(username)
        if not user:
            return False
        
        if not user.check_password(password):
            return False

        return True
 
    @classmethod
    def update(cls, user_id: int, first_name:str, last_name:str, is_active: bool) -> "UserModel":
        """ Update a user's is_active """
        user = cls.get_by_id(user_id)
        user.is_active = is_active
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return user

    @staticmethod
    def create(username: str, email:str, password:str, first_name:str, last_name:str) -> "UserModel":
        """ Create a new user """
        user = UserModel()
        user.username = username
        user.email = email
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return user

    @classmethod
    def send_confirmation_email(cls, user_id) -> Response:
        user = cls.get_by_id(user_id)
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + url_for(
            "auth.confirmemailresource", confirmation_id=user.most_recent_confirmation.id
        )
        #link=""
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        return SendMail.send_email([user.email], subject, text, html)


class EmailConfirmationService:

    @staticmethod
    def get_by_id(confirmation_id: str) -> "EmailConfirmationModel":
        """ Query a email confirmation by id """
        return EmailConfirmationModel.query.filter_by(id=confirmation_id).first()

    @staticmethod
    def get_all() -> "EmailConfirmationModel":
        """ Query all email confirmation """
        return EmailConfirmationModel.query.all()

    @classmethod
    def expired(cls, confirmation_id: str) -> bool:
        """ Check if expired """
        confirmation = cls.get_by_id(confirmation_id)
        if confirmation:
            return time() > confirmation.expire_at
    
    @classmethod
    def force_to_expire(cls, confirmation_id: str) -> "EmailConfirmationModel":  
        """ Forcing current confirmation to expire """
        if not cls.expired(confirmation_id):
            confirmation = cls.get_by_id(confirmation_id)
            confirmation.expire_at = int(time())
            confirmation.save()
            return confirmation
    
    @classmethod
    def confirm_email(cls, confirmation_id: str) -> "EmailConfirmationModel":
        """ Confirm the email """
        confirmation = cls.get_by_id(confirmation_id)
        confirmation.confirmed = True
        confirmation.save()
        return confirmation

    @staticmethod
    def create(user_id: int) -> "EmailConfirmationModel":
        """ Create a new user """
        confirmation = EmailConfirmationModel(user_id=user_id)
        confirmation.save()
        return confirmation


class AuthTokenService:

    @classmethod
    def encode_auth_token(cls, user_id:str):
        """Create a token with user_id and expiration date using secret key"""
        exp_seconds = config.AUTH_TOKEN_EXPIRATION_SECONDS
        exp_date = datetime.now() + timedelta(seconds=exp_seconds)
        payload = {"exp": exp_date, "iat": datetime.now(), "sub": user_id}
        return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256").decode("utf-8")

    @classmethod
    def decode_auth_token(cls, token:str):
        """Convert token to original payload using secret key if the token is valid"""
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithm="HS256", options={'verify_exp': False})
            return payload
        except jwt.InvalidTokenError as ex:
            raise InvalidTokenError() from ex

    @classmethod
    def get_token_from_header(cls) -> str:
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                token = None
        return token

    @classmethod
    def blacklist_token(cls, token:str) -> "BlacklistTokenModel":
        bl_token = BlacklistTokenModel(token)
        bl_token.save()
        return bl_token

    @classmethod
    def is_token_blacklisted(cls, token:str) -> bool:
        bl_token = BlacklistTokenModel.query.filter_by(token=token).first()
        return True if bl_token else False


def auth_required(f):
    """Decorator to require auth token on marked endpoint"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = AuthTokenService.get_token_from_header()
        if not token:
            raise InvalidTokenError()

        if AuthTokenService.is_token_blacklisted(token):
            raise TokenExpiredError()

        token_payload = AuthTokenService.decode_auth_token(token)

        current_user = UserService.get_by_id(token_payload["sub"])
        if not current_user:
            raise InvalidTokenError()

        return f(*args, **kwargs)

    return decorated_function