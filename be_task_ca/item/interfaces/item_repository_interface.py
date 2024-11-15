from typing import List, Optional
from uuid import UUID
from abc import ABC, abstractmethod
from ..entities.item import Item

class ItemRepositoryInterface(ABC):
    """???"""

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        """???"""
        pass

    @abstractmethod
    def find_item_by_name(self, name: str) -> Optional[Item]:
        """???"""
        pass

    @abstractmethod
    def find_item_by_id(self, id: UUID) -> Item:
        """???"""
        pass

    @abstractmethod
    def save_item(self, item: Item) -> Item:
        """???"""
        pass