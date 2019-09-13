import os
from main.config import config_by_name
config = config_by_name[os.getenv('APP_ENV') or 'dev']

if config.EMAIL_BACKEND == "mailgun":
    from .mailgun import Mailgun as SendMail
    from .mailgun import MailGunException as SendMailException
elif config.EMAIL_BACKEND == "sendgrid":
    from .sendgrid import Sendgrid as SendMail
    from .sendgrid import SendgridException as SendMailException
else:
    from .console import Console as SendMail
    from .console import ConsoleException as SendMailException