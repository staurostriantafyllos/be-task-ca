from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str | None = None
    price: float
    quantity: int
