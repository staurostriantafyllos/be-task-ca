from typing import List, Optional
from uuid import UUID
from abc import ABC, abstractmethod
from ..entities.user import User, CartItem

class UserRepositoryInterface(ABC):
    """Interface for User repository."""

    @abstractmethod
    def find_user_by_email(self, email: str) -> Optional[User]:
        """Finds a user by its email."""
        pass

    @abstractmethod
    def find_user_by_id(self, id: UUID) -> User:
        """Finds a user by its ID."""
        pass

    @abstractmethod
    def save_user(self, user: User) -> User:
        """Saves a new user."""
        pass

    @abstractmethod
    def save_cart_item(self, cart_item: CartItem) -> CartItem:
        """Saves a new cart item."""
        pass

    @abstractmethod
    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        """Gets all items in user cart."""
        pass