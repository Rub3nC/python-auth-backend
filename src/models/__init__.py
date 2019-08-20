from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .auth import UserModel, ConfirmationModel