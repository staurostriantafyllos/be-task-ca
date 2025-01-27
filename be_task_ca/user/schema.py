from typing import List
from uuid import UUID
from pydantic import BaseModel


class ItemQuantity(BaseModel):
    item_id: UUID
    quantity: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    shipping_address: str | None


class UserPrivate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    cart_items: List[ItemQuantity] = []

    class Config:
        orm_mode = True


class AddToCartResponse(BaseModel):
    items: List[ItemQuantity]
