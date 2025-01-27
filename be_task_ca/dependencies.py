from typing import Dict, List
from uuid import UUID

from .item.model import Item
from .item.repository import ItemRepoInMemory
from .user.model import User, CartItem
from .user.repository import UserRepoInMemory

items: Dict[UUID, Item] = {}
users: Dict[UUID, User] = {}
cart_items: Dict[UUID, List[CartItem]] = {}


def get_user_repo():
    """Dependency to provide UserRepo."""
    return UserRepoInMemory(users, cart_items)


def get_item_repo():
    """Dependency to provide ItemRepo."""
    return ItemRepoInMemory(items)
