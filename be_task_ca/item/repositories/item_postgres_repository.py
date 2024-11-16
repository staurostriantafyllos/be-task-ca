from dataclasses import asdict
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from .model import Item as ItemModel
from ..entities.item import Item
from ..interfaces.item_repository_interface import ItemRepositoryInterface

class ItemPostgresRepository(ItemRepositoryInterface):
    """Repository implementation for Item using Postgres"""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_items(self) -> List[Item]:
        """Retrieves all items."""

        item_list = self.db_session.query(ItemModel).all()
        return [Item(**asdict(item_model)) for item_model in item_list]

    def find_item_by_name(self, name: str) -> Optional[Item]:
        """Finds an item by its name."""

        item_model = self.db_session.query(ItemModel).filter(ItemModel.name == name).first()

        if item_model is None:
            return None

        return Item(**asdict(item_model))

    def find_item_by_id(self, id: UUID) -> Item:
        """Finds an item by its ID."""

        item_model = self.db_session.query(ItemModel).filter(ItemModel.id == id).first()

        if item_model is None:
            return None

        return Item(**asdict(item_model))

    def save_item(self, item: Item) -> Item:
        """Saves a new item."""

        item_model = ItemModel(**asdict(item))

        self.db_session.add(item_model)
        self.db_session.commit()
        self.db_session.refresh(item_model)

        return Item(**asdict(item_model))
