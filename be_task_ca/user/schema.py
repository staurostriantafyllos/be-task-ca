from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ItemQuantity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: UUID
    quantity: int


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    shipping_address: str | None


class UserPrivate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    cart_items: List[ItemQuantity] = []


class AddToCartResponse(BaseModel):
    items: List[ItemQuantity]
