import json


class UserAlreadyExistsError(Exception):
    pass


class UserDoesNotExistError(Exception):
    pass


class ItemDoesNotExistError(Exception):
    pass


class ItemAlreadyExistsError(Exception):
    pass


class ItemQuantityError(Exception):
    pass


class ItemAlreadyInCartError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class TokenMalformedError(Exception):
    pass


class TokenInvalidError(Exception):
    pass


class UserException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        try:
            self.message = json.loads(message)  # Try parsing as JSON
        except (json.JSONDecodeError, TypeError):
            self.message = {"error": message}
        super().__init__(message)


class UserSignupError(UserException):
    pass


class UserLoginError(UserException):
    pass


class UserTokenRefreshException(UserException):
    pass
