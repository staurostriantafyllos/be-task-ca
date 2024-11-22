class UserAlreadyExistsError(Exception):
    """Triggered when attempting to create a user that already exists."""

    def __init__(self, email: str):
        self.email = email
        message = f"A user with the email '{email}' already exists."
        super().__init__(message)

class UserDoesNotExistError(Exception):
    """Triggered when a user doesn't exist."""

    def __init__(self):
        message = "Provided user doesn't exist."
        super().__init__(message)


class ItemAlreadyInCartError(Exception):
    """Raised when the item is already in the user's cart."""

    def __init__(self):
        message = "The item is already in the user's cart."
        super().__init__(message)
