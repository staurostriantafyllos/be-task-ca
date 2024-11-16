from typing import List
from uuid import UUID
from ..entities.user import User
from ..entities.cart_item import CartItem
from ..interfaces.user_repository_interface import UserRepositoryInterface
from ..exceptions import UserAlreadyExistsError, UserDoesNotExistError, ItemAlreadyInCartError
from ...item.entities.item import Item
from ...item.interfaces.item_repository_interface import ItemRepositoryInterface
from ...item.exceptions import ItemDoesNotExistError

def create_user(user: User, repo: UserRepositoryInterface) -> User:
    """Create a new user if it doesn't exist in the repository."""

    if repo.find_user_by_email(user.email):
        raise UserAlreadyExistsError(user.email) # Adding a generic exception to avoid coupling with the framework (HTTPException)
    return repo.save_user(user)

def add_item_to_cart(
        cart_item: CartItem,
        user_repo: UserRepositoryInterface,
        item_repo: ItemRepositoryInterface
) -> List[CartItem]:
    """Adds a new cart item for the specified user."""

    user: User = user_repo.find_user_by_id(cart_item.user_id)

    if user is None:
        raise UserDoesNotExistError()

    item: Item = item_repo.find_item_by_id(cart_item.item_id)
    if item is None:
        raise ItemDoesNotExistError()

    existing_cart_item = next((ci for ci in user.cart_items if ci["item_id"] == cart_item.item_id), None)
    if existing_cart_item:
        raise ItemAlreadyInCartError()

    user_repo.save_cart_item(cart_item)

    return user_repo.find_cart_items_for_user_id(user.id)


def list_items_in_cart(user_id: UUID, user_repo: UserRepositoryInterface) -> List[CartItem]:
    """Retrieves the list of items in the user cart."""
    return user_repo.find_cart_items_for_user_id(user_id)