import traceback
from marshmallow import ValidationError
from flask_restful import Resource
from flask import request
from schemas import UserSchema, UserRegistrationSchema
from services import UserService, EmailConfirmationService

from libs import SendMailException


USER_ALREADY_EXISTS = "A user with that username already exists."
EMAIL_ALREADY_EXISTS = "A user with that email already exists."
FAILED_TO_CREATE = "Internal server error. Failed to create user."
CONFIRMATION_NOT_FOUND = "Confirmation reference not found."
CONFIRMATION_LINK_EXPIRED = "The link has expired."
CONFIRMATION_ALREADY_CONFIRMED = "Registration has already been confirmed."
CONFIRMATION_SUCCESS = "Email Confirmation Success"


class UserResource(Resource):
    # post -> To create a user
    def post(self):
        user_schema_register = UserRegistrationSchema()
        user_json = request.get_json()
        try:
            user = user_schema_register.load(user_json)
        except ValidationError as e:
            return e.messages

        if UserService.get_by_username(user["username"]):
            return {"message": USER_ALREADY_EXISTS}, 400

        if UserService.get_by_email(user["email"]):
            return {"message": EMAIL_ALREADY_EXISTS}, 400

        try:
            user = UserService.create(
                user["username"],
                user["email"],
                user["password"],
                user["first_name"],
                user["last_name"],
            )
            confirmation = EmailConfirmationService.create(user.id)
            UserService.send_confirmation_email(user.id)
            user_schema = UserSchema()
            return user_schema.dump(user), 201
        except SendMailException as e:
            user.delete()  # rollback
            return {"message": str(e)}, 500
        except:  # failed to save user to db
            traceback.print_exc()
            if user:
                user.delete()
            return {"message": FAILED_TO_CREATE}, 500

    # get -> Return user profile. Access_token require
    def get(self):
        # Response data profile
        return {"message": "Data User Profile"}, 200

    # put -> To update user information. Not valid to password. Access_token require
    def put(self):
        # Received and check data
        # If data not valid prepare error message and send
        # If data valid update user information
        # Response
        return {"message": "Update User"}, 200

class UserLoginResource(Resource):
    # post -> To log in a user
    def post(self):
        # Receive and check data
        # If data no valid prepare error message an send
        # If data is valid but not user register send message User not found
        # If data is valid and user register,verify is confirm email is confirmed
        # If all ok create access_token and refresh token
        # Response
        return {"message": "Logged in user"}, 200

class UserLogoutResource(Resource):
    # post -> To log out a user. Access_token require
    def post(self):
        # Check access_token and the identity user
        # If no valid user prepare error message
        # If valid log out user
        # Response
        return {"message": "Logout in user"}, 200

class ConfirmEmailResource(Resource):
    # get -> To receive email confirmations
    def get(self):
        confirmation_id = request.args.get("confirmation_id", "")
        confirmation = EmailConfirmationService.get_by_id(confirmation_id)
        if not confirmation:
            return {"message": CONFIRMATION_NOT_FOUND}, 404

        if EmailConfirmationService.expired(confirmation_id):
            return {"message": CONFIRMATION_LINK_EXPIRED}, 400

        if confirmation.confirmed:
            return {"message": CONFIRMATION_ALREADY_CONFIRMED}, 400

        confirmation.confirmed = True
        confirmation.save()

        return {"message": CONFIRMATION_SUCCESS}, 200

    # post -> To send a resend email. Register user require
    def post(self, confirmation_id: str):
        # Receive and check user data
        # If not valid or user no found prepare error message
        # Send confirm email
        # Response
        return {"message": "Send confirm email"}, 200

class ChangePasswordResource(Resource):
    # post -> To change user password. Register user require
    def post(self):
        # Receive and check data {email or username}
        # If not valid or not found prepare error message
        # If valid send email to reset password
        return {"message": "Password Change"}, 200

class ResetPasswordResource(Resource):
    # get -> To receive a request from the password change email. 
    # Valid password change email token require
    def get(self):
        # Check request token from password change email
        # If not valid prepare error message
        # If valid prepare form to change pasword
        return {"message": "Show password change form"}, 200

    # post -> To change user password. Register user require
    def post(self):
        # Receive data {password}
        # If not valid prepare error message
        # If valid update user password
        return {"message": "Udate Password"}, 200

class VerifyTokenResource(Resource):
    # post -> To verify JWT token. Access_token require
    def post(self):
        # Check access_token and the identity user
        # If not valid or not found prepare error message
        # If valid send current access_token
        return {"message": "Verify Token"}, 200

class TokenRefreshResource(Resource):
    # post -> To send a new access_token. refresh_token require
    def post(self):
        # Check refresh_token and the identity user
        # If not valid or not found prepare error message
        # If valid send a new access_token        
        return {"message": "New Access Token"}, 200

class AuthorizeDeviceResource(Resource):
    # post -> Authorizes the user to log in from a new device. Register user require
    def post(self):
        # I don't know the process
        return {"message": "Authorize Device"}, 200

class UserListResource(Resource):
    # get -> Return a user list. Admin user require
    def get(self):
        # Verify user.
        # If not admin user prepare error message
        # If admin user send user list
        return {"message": "User list"}, 200

class SpecificUserResource(Resource):
    # get -> Return user profile. Admin user require
    def get(self, user_id: int):
    	# Verify user.
        # If not admin user or user_id not found prepare error message
        # If admin user and user_id found send user information
        return {"message": "Data a Specific User Profile"}, 200

    # put -> To update user information. Admin user require
    def put(self, user_id: int):
        # Verify user.
        # If not admin user or user_id not found prepare error message
        # If admin user and user_id found send update user information
        return {"message": "Update a Specific User"}, 200

    # delete -> To delete a user
    def delete(self, user_id: int):
        # Verify user.
        # If not admin user or user_id not found prepare error message
        # If admin user and user_id found delete user
        return {"message": "Delete a user"}, 200