from typing import List, Optional
from uuid import UUID, uuid4
from ..entities.item import Item
from ..interfaces.item_repository_interface import ItemRepositoryInterface

class ItemInMemoryRepository(ItemRepositoryInterface):
    """In-memory repository implementation for Item"""

    items = [] # Static class attribute to store items

    def get_all_items(self) -> List[Item]:
        """Retrieves all items."""

        return self.items

    def find_item_by_name(self, name: str) -> Optional[Item]:
        """Finds an item by its name."""

        return next((item for item in self.items if item.name == name), None)

    def find_item_by_id(self, id: UUID) -> Item:
        """Finds an item by its ID."""

        return next((item for item in self.items if item.id == id), None)

    def save_item(self, item: Item) -> Item:
        """Saves a new item."""

        item.id = uuid4()
        self.items.append(item)

        return item
