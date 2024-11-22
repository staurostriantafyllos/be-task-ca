from typing import Optional, List
from uuid import UUID, uuid4
from ..entities.user import User, CartItem
from ..interfaces.user_repository_interface import UserRepositoryInterface

class UserInMemoryRepository(UserRepositoryInterface):
    """Repository implementation for Item using Postgres"""

    users = []
    cart_items = []

    def find_user_by_email(self, email: str) -> Optional[User]:
        """Finds a user by its email."""

        return next((user for user in self.users if user.email == email), None)

    def find_user_by_id(self, id: UUID) -> User:
        """Finds a user by its ID."""

        return next((user for user in self.users if user.id == id), None)

    def save_user(self, user: User) -> User:
        """Saves a new user."""

        user.id = uuid4()
        self.users.append(user)
        return user

    def save_cart_item(self, cartitem: CartItem) -> CartItem:
        """Saves a new cart item."""

        self.cart_items.append(cartitem)
        return cartitem

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        """Gets all items in user cart."""

        return [cartitem for cartitem in self.cart_items if cartitem.user_id == user_id]