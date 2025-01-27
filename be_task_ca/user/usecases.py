from typing import List
from uuid import UUID

from ..exceptions import (
    ItemAlreadyInCartError,
    ItemDoesNotExistError,
    ItemQuantityError,
    UserAlreadyExistsError,
    UserDoesNotExistError,
)
from .repository import UserRepo

from ..item.repository import ItemRepo

from .schema import (
    ItemQuantity,
    UserPrivate,
    User,
)


def create_user(user_repo: UserRepo, create_user: UserPrivate) -> User:
    search_result = user_repo.find_user_by_email(create_user.email)
    if search_result is not None:
        raise UserAlreadyExistsError("An user with this email address already exists")

    new_user = user_repo.save_user(create_user)

    return new_user


def add_item_to_cart(
    user_repo: UserRepo,
    item_repo: ItemRepo,
    user_id: UUID,
    cart_item: ItemQuantity,
) -> List[ItemQuantity]:
    user = user_repo.find_user_by_id(user_id)
    if user is None:
        raise UserDoesNotExistError("User does not exist")

    item = item_repo.find_item_by_id(cart_item.item_id)
    if item is None:
        raise ItemDoesNotExistError("Item does not exist")

    if item.quantity < cart_item.quantity:
        raise ItemQuantityError("Not enough items in stock")

    item_ids = [o.item_id for o in user.cart_items]
    if cart_item.item_id in item_ids:
        raise ItemAlreadyInCartError("Item already in cart")

    user_repo.update_user_cart_items(user_id, cart_item)

    return user_repo.list_items_in_cart(user.id)


def list_items_in_cart(user_repo: UserRepo, user_id: UUID) -> List[ItemQuantity]:
    user = user_repo.find_user_by_id(user_id)
    if user is None:
        raise UserDoesNotExistError("User does not exist")

    return user_repo.list_items_in_cart(user.id)
