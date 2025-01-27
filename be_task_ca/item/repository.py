from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from .schema import ItemBase, Item as ItemSchema
from .model import Item


class ItemRepo(ABC):
    @abstractmethod
    def save_item(self, item: ItemBase) -> ItemSchema:
        """
        Save an item to the database.
        """
        pass

    @abstractmethod
    def get_all_items(self) -> List[ItemSchema]:
        """
        Retrieve all items from the database.
        """
        pass

    @abstractmethod
    def find_item_by_name(self, name: str) -> ItemSchema | None:
        """
        Find an item by its name.
        """
        pass

    @abstractmethod
    def find_item_by_id(self, id: UUID) -> ItemSchema | None:
        """
        Find an item by its ID.
        """
        pass


class ItemRepoInMemory(ItemRepo):
    def __init__(self, items: dict[UUID, Item]):
        self.items = items

    def save_item(self, item: ItemBase) -> ItemSchema:
        new_item = Item(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        self.items[new_item.id] = new_item

        return ItemSchema.model_validate(new_item)

    def get_all_items(self) -> List[ItemSchema]:
        items = list(self.items.values())
        return [ItemSchema.model_validate(item) for item in items]

    def find_item_by_name(self, name: str) -> ItemSchema | None:
        for item in self.items.values():
            if item.name == name:
                return ItemSchema.model_validate(item)
        return None

    def find_item_by_id(self, id: UUID) -> ItemSchema | None:
        item = self.items.get(id)
        if not item:
            return None
        return ItemSchema.model_validate(item)
