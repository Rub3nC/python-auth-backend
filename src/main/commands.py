from flask_script import Command
from marshmallow import ValidationError

from schemas import UserRegistrationSchema
from services import UserService
from models import UserModel

ADMIN_USER_ALREADY_EXISTS = "A admin user with that username already exists."
ADMIN_EMAIL_ALREADY_EXISTS = "A admin user with that email already exists."
ADMIN_CREATE_SUCCESSFUL = "Admin user successfully create."


class CreateAdminUser(Command):
    
    def run(self):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
         
        user_schema = UserRegistrationSchema(only=("password","email"))
        data = {
            "password": password,
            "email": email
        }
        try:
            user = user_schema.load(data)
            if UserService.get_by_username(username):
                print(ADMIN_USER_ALREADY_EXISTS)
            elif UserService.get_by_email(email):
                print(ADMIN_EMAIL_ALREADY_EXISTS)
            else:
                user = UserModel()
                user.username = username
                user.email = email
                user.password = password
                user.is_admin = True
                user.save()

                print()
        except ValidationError as e:
            print (e.messages)