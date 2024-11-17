from dataclasses import asdict
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from .model import User as UserModel, CartItem as CartItemModel
from ..entities.user import User, CartItem
from ..interfaces.user_repository_interface import UserRepositoryInterface

class UserPostgresRepository(UserRepositoryInterface):
    """Repository implementation for Item using Postgres"""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_user_by_email(self, email: str) -> Optional[User]:
        """Finds a user by its email."""

        user_model = self.db_session.query(UserModel).filter(UserModel.email == email).first()

        if user_model is None:
            return None

        return User(**asdict(user_model))

    def find_user_by_id(self, id: UUID) -> User:
        """Finds a user by its ID."""

        user_model = self.db_session.query(UserModel).filter(UserModel.id == id).first()

        if user_model is None:
            return None

        return User(**asdict(user_model))

    def save_user(self, user: User) -> User:
        """Saves a new user."""

        user_model = UserModel(**asdict(user))

        self.db_session.add(user_model)
        self.db_session.commit()
        self.db_session.refresh(user_model)

        return User(**asdict(user_model))

    def save_cart_item(self, cartitem: CartItem) -> CartItem:
        """Saves a new cart item."""

        cartitem_model = CartItemModel(**asdict(cartitem))

        self.db_session.add(cartitem_model)
        self.db_session.commit()
        self.db_session.refresh(cartitem_model)

        return CartItem(**asdict(cartitem_model))

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        """Gets all items in user cart."""

        cartitem_models = self.db_session.query(CartItemModel).filter(CartItemModel.user_id == user_id).all()
        return [CartItem(**asdict(cartitem)) for cartitem in cartitem_models]