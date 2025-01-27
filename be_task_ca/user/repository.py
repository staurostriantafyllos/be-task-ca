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
    def find_user_by_id(self, id: UUID) -> UserSchema:
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


class UserRepoSA(UserRepo):
    def __init__(self, db):
        self.db = db

    def save_user(self, user: UserPrivate) -> UserSchema:
        user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
        )
        self.db.add(user)
        self.db.commit()

        return UserSchema.model_validate(user)

    def update_user_cart_items(self, user_id, cart_item: ItemQuantity) -> ItemQuantity:
        new_cart_item = CartItem(
            user_id=user_id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
        )
        self.db.add(new_cart_item)
        self.db.commit()

        return ItemQuantity.model_validate(new_cart_item)

    def find_user_by_email(self, email: str) -> UserSchema | None:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return
        return UserSchema.model_validate(user)

    def find_user_by_id(self, id: UUID) -> UserSchema | None:
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            return
        return UserSchema.model_validate(user)

    def list_items_in_cart(self, user_id) -> List[ItemQuantity]:
        cart_items = self.db.query(CartItem).filter(CartItem.user_id == user_id).all()
        return [ItemQuantity.model_validate(item) for item in cart_items]
