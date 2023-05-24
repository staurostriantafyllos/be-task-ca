"""
Clean Architecture: 
The domain models should not be aware of database implementation details. 
Right now we have leakage from repository into domain.
So, we should remove the SQLAlchemy related code from our models.
It's good that we can use some annotations or tools related to the ORM being used, but ideally we,
should have separate DAO and DTO and have the other advantages too.
We should consider applying DDD principles to better isolate the domains and make the dependencies between them more explicit. 
Each bounded context (User, Item) should have its own domain model and shouldn't directly depend on other domains.

General:
It's better to be consistent throghout the code base, here we import UUID and uuid4 separately,
but in user/model.py we import uuid directly and use it. Also the imports should adhere to the notes inside item/api.py
"""

from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from be_task_ca.database import Base


@dataclass
class Item(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4(),
        index=True,
    )
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]
