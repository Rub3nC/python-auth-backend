import os
import json
from typing import List
from requests import Response, post
from main.config import config_by_name

config = config_by_name[os.getenv('APP_ENV') or 'dev']

FAILED_LOAD_API_KEY = "Failed to load MailGun API key."
FAILED_LOAD_DOMAIN = "Failed to load MailGun domain."
ERROR_SENDING_EMAIL = "Error in sending confirmation email, user registration failed."


class SendgridException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Sendgrid:
    SENDGRID_API_KEY = config.SENDGRID_API_KEY

    FROM_TITLE = "Auth REST API"
    FROM_EMAIL = f"auth_api@example.com"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        if cls.SENDGRID_API_KEY is None:
            raise SendgridException(FAILED_LOAD_API_KEY)

        headers = {
            'Authorization': 'Bearer {}'.format(cls.SENDGRID_API_KEY),
            'Content-Type': 'application/json',
        }
        
        emails = []
        for mail in email:
            emails.append({'email': mail})

        data = {
                'personalizations': [
                    {
                        'to': emails,
                    }
                ],
                'subject': subject,
                'from': {
                    'email': f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>"
                },
                'content': [
                    {
                        'type': 'text/plain',
                        'value': text
                    },
                    {
                        'type': 'text/html',
                        'value': html
                    },

                ]
            }
        response = post(
            "https://api.sendgrid.com/v3/mail/send",
            headers=headers,
            data = json.dumps(data)
        )

        if response.status_code != 202:
            raise SendgridException(ERROR_SENDING_EMAIL)

        return response
