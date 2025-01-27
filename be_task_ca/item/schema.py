from typing import List
from uuid import UUID
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int


class Item(ItemBase):
    id: UUID

    class Config:
        orm_mode = True


class AllItemsRepsonse(BaseModel):
    items: List[Item]
