class ItemAlreadyExistsError(Exception):
    """Triggered when attempting to create an item that already exists."""

    def __init__(self, item_name: str):
        self.item_name = item_name
        message = f"An item with the name '{item_name}' already exists."
        super().__init__(message)

class ItemDoesNotExistError(Exception):
    """Triggered when an item doesn't exist."""

    def __init__(self):
        message = "Provided item doesn't exist."
        super().__init__(message)