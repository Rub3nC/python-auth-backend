import os
import json
from requests import Response
from typing import List
from main.config import config_by_name

config = config_by_name[os.getenv('APP_ENV') or 'dev']

FAILED_LOAD_API_KEY = "Failed to load MailGun API key."
FAILED_LOAD_DOMAIN = "Failed to load MailGun domain."
ERROR_SENDING_EMAIL = "Error in sending confirmation email, user registration failed."


class ConsoleException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Console:
    FROM_TITLE = "Auth REST API"
    FROM_EMAIL = f"auth_api@example.com"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:

        print("----------------------------------------------\n")
        print("\t\t Email {}\n".format(cls.FROM_TITLE))
        print("----------------------------------------------\n\n")
        print("From: {}\n".format(cls.FROM_EMAIL))
        print("To: {}\n".format(email))
        print("Subject: {}\n\n\n".format(subject))
        print(text)
        print("\n\n")

        return 200
