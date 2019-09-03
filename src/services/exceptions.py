from flask import jsonify


class AppError(Exception):
    """Base class for all errors. Can represent error as HTTP response for API calls"""

    status_code = 500
    message = "Request cannot be processed at the moment."

    def __init__(self, status_code=None, message=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_api_response(self):
        response = jsonify(
            {"message": self.message}
        )
        response.status_code = self.status_code
        return response


class InvalidTokenError(AppError):
    def __init__(self):
        AppError.__init__(
            self,
            status_code=401,
            message="Token is invalid or missing.",
        )


class TokenExpiredError(AppError):
    def __init__(self):
        AppError.__init__(
            self,
            status_code=401,
            message="Authentication token has expired.",
        )