from dataclasses import dataclass
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


@dataclass
class CartItem(Base):
    __tablename__ = "cart_items"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )
    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column()


@dataclass
class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    shipping_address: Mapped[str | None] = mapped_column(default=None, nullable=True)
    cart_items: Mapped[List["CartItem"]] = relationship()
