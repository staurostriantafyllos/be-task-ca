from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


@dataclass
class Item(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str | None] = mapped_column(default=None, nullable=True)
    price: Mapped[float] = mapped_column()
    quantity: Mapped[int] = mapped_column()
