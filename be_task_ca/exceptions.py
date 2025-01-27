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
