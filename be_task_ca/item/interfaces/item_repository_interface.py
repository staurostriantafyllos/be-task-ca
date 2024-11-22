from typing import List, Optional
from uuid import UUID
from abc import ABC, abstractmethod
from ..entities.item import Item

class ItemRepositoryInterface(ABC):
    """Interface for Item repository."""

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        """Retrieves all items."""
        pass

    @abstractmethod
    def find_item_by_name(self, name: str) -> Optional[Item]:
        """Finds an item by its name."""
        pass

    @abstractmethod
    def find_item_by_id(self, id: UUID) -> Item:
        """Finds an item by its ID."""
        pass

    @abstractmethod
    def save_item(self, item: Item) -> Item:
        """Saves a new item."""
        pass