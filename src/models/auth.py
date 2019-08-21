import os
from datetime import datetime
from time import time
from uuid import uuid4
from . import db
from .base import BaseModel
from main.config import config_by_name

config = config_by_name[os.getenv('APP_ENV') or 'dev']

                            # 60seg*36min*24h = 1d 
CONFIRMATION_EXPIRATION_DELTA = 60*60*24*int(config.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS)

class UserModel(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True, unique=True)
    password_hash = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(80), nullable=True, unique=True)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)

    confirmation = db.relationship(
        "EmailConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __init__(self):
        self.created_at = datetime.now()
        self.update_at = datetime.now()
        self.is_active = True


class EmailConfirmationModel(db.Model, BaseModel):
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False
        self.created_at = datetime.now()