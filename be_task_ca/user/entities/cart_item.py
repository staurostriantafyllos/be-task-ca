from dataclasses import dataclass
import uuid

@dataclass
class CartItem:
    """CartItem domain entity definition."""
    user_id: uuid.UUID
    item_id: uuid.UUID
    quantity: int