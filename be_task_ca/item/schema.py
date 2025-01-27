from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class AllItemsRepsonse(BaseModel):
    items: List[Item]
