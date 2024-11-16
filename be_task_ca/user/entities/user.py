from typing import List, Optional
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .cart_item import CartItem

@dataclass
class User:
    """User domain entity definition."""
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: Optional[str] = None
    cart_items: List[CartItem] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)