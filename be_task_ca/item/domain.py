from dataclasses import dataclass, field
from uuid import UUID, uuid4
# from sqlalchemy.orm import Mapped, mapped_column
# from be_task_ca.database import Base


# @dataclass
# class Item(Base):
#     __tablename__ = "items"

#     id: Mapped[UUID] = mapped_column(
#         primary_key=True,
#         default=uuid4(),
#         index=True,
#     )
#     name: Mapped[str] = mapped_column(unique=True, index=True)
#     description: Mapped[str]
#     price: Mapped[float]
#     quantity: Mapped[int]


@dataclass
class Item:
    """???"""

    name: str
    description: str
    price: float
    quantity: int
    id: UUID = field(default_factory=uuid4)

    # def __post_init__(self):
    #     if self.price < 0:
    #         raise ValueError("Price must be non-negative")
    #     if self.quantity < 0:
    #         raise ValueError("Quantity must be non-negative")