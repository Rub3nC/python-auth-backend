from time import time
from models import UserModel, EmailConfirmationModel


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
    def update(cls, user_id: int, first_name:str, last_name:str, is_active: bool) -> "UserModel":
        """ Update a user's is_active """
        user = cls.get_by_id(user_id)
        user.is_active = is_active
        user.first_name = first_name
        user.last_name = last_name

        return user.save()

    @staticmethod
    def create(username: str, email:str, password:str, first_name:str, last_name:str) -> "UserModel":
        """ Create a new user """
        user = UserModel()
        user.username = username
        user.email = email
        user.password = password
        user.first_name = first_name
        user.last_name = last_name

        return user.save()


class EmailConfirmationService:

    @staticmethod
    def get_by_id(confimation_id: str) -> "EmailConfirmationModel":
        """ Query a email confirmation by id """
        return EmailConfirmationModel.query.filter_by(id=confimation_id).first()

    @staticmethod
    def get_all() -> "EmailConfirmationModel":
        """ Query all email confirmation """
        return EmailConfirmationModel.query.all()

    @classmethod
    def expired(cls, confimation_id: str) -> bool:
        ''' Check if expired '''
        confirmation = cls.get_by_id(confimation_id)
        if confirmation:
            return time() > confirmation.expire_at
    
    @classmethod
    def force_to_expire(cls, confimation_id: str) -> "EmailConfirmationModel":  
        ''' Forcing current confirmation to expire '''
        if not cls.expired(confimation_id):
            confirmation = cls.get_by_id(confimation_id)
            confirmation.expire_at = int(time())
            return confirmation.save()
    
    @classmethod
    def confirme(cls, confimation_id: str) -> "EmailConfirmationModel":
        ''' Confirm the email '''
        confirmation = cls.get_by_id(confimation_id)
        confirmation.confirmed = True
        return confirmation.save()

    @staticmethod
    def create(user_id: int) -> "EmailConfirmationModel":
        """ Create a new user """
        confirmation = EmailConfirmationModel(user_id=user_id)

        return confirmation.save()