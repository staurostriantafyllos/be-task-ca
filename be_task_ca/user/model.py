from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List


class CartItem(BaseModel):
    user_id: UUID
    item_id: UUID
    quantity: int


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: str | None = None
    cart_items: List[CartItem] = []
