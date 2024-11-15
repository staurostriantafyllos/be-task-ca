class ItemAlreadyExistsError(Exception):
    """Triggered when attempting to create an item that already exists."""

    def __init__(self, item_name: str):
        self.item_name = item_name
        message = f"An item with the name '{item_name}' already exists."
        super().__init__(message)