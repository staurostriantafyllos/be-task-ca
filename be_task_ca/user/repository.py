from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from .schema import (
    ItemQuantity,
    UserPrivate,
    User as UserSchema,
)
from .model import CartItem, User


class UserRepo(ABC):
    @abstractmethod
    def save_user(self, user: UserPrivate) -> UserSchema:
        """
        Save a new user to the database.
        """
        pass

    @abstractmethod
    def update_user_cart_items(
        self, user_id: UUID, cart_item: ItemQuantity
    ) -> ItemQuantity:
        """
        Add an item in the user's cart.
        """
        pass

    @abstractmethod
    def find_user_by_email(self, email: str) -> UserSchema | None:
        """
        Find a user by their email address.
        """
        pass

    @abstractmethod
    def find_user_by_id(self, id: UUID) -> UserSchema | None:
        """
        Find a user by their unique ID.
        """
        pass

    @abstractmethod
    def list_items_in_cart(self, user_id: UUID) -> List[ItemQuantity]:
        """
        List all items in a user's cart.
        """
        pass


class UserRepoInMemory(UserRepo):
    def __init__(self, users, cart_items):
        self.users = users
        self.cart_items = cart_items

    def save_user(self, user: UserPrivate) -> UserSchema:
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
        )
        self.users[new_user.id] = new_user
        self.cart_items[new_user.id] = []
        return UserSchema.model_validate(new_user)

    def update_user_cart_items(
        self, user_id: UUID, cart_item: ItemQuantity
    ) -> ItemQuantity:
        new_cart_item = CartItem(
            user_id=user_id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
        )
        self.cart_items[user_id].append(new_cart_item)
        return ItemQuantity.model_validate(new_cart_item)

    def find_user_by_email(self, email: str) -> UserSchema | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def find_user_by_id(self, id: UUID) -> UserSchema | None:
        user = self.users.get(id)
        if not user:
            return None
        return UserSchema.model_validate(user)

    def list_items_in_cart(self, user_id: UUID) -> List[ItemQuantity]:
        cart_items = self.cart_items.get(user_id, [])
        return [ItemQuantity.model_validate(item) for item in cart_items]
