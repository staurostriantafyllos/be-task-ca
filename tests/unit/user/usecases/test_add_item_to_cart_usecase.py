from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from be_task_ca.exceptions import (
    ItemAlreadyInCartError,
    ItemDoesNotExistError,
    ItemQuantityError,
    UserDoesNotExistError,
)
from be_task_ca.item.repository import ItemRepo
from be_task_ca.item.schema import Item
from be_task_ca.user.repository import UserRepo
from be_task_ca.user.schema import ItemQuantity, User
from be_task_ca.user.usecases import add_item_to_cart


@pytest.fixture
def user_repo():
    return MagicMock(spec=UserRepo)


@pytest.fixture
def item_repo():
    return MagicMock(spec=ItemRepo)


@pytest.fixture
def user(item_in_cart):
    return User(
        id=uuid4(),
        email="",
        first_name="",
        last_name="",
        shipping_address="",
        cart_items=[
            ItemQuantity(item_id=item_in_cart.id, quantity=1),
        ],
    )


@pytest.fixture
def item():
    return Item(
        id=UUID("72b53c6d-62d1-4225-91f8-9d993058996d"),
        name="test-item",
        price=10.0,
        quantity=5,
    )


@pytest.fixture
def item_in_cart():
    return Item(
        id=UUID("4861774c-9d73-4584-9994-caf5963c9c34"),
        name="test-item-in-cart",
        price=10.0,
        quantity=5,
    )


@pytest.fixture
def new_cart_item(item):
    return ItemQuantity(item_id=item.id, quantity=item.quantity - 1)


@pytest.fixture
def existing_cart_item(item_in_cart):
    return ItemQuantity(item_id=item_in_cart.id, quantity=item_in_cart.quantity - 2)


def test_add_item_to_cart_when_the_user_does_not_exist(
    user_repo, item_repo, user, new_cart_item
):
    user_repo.find_user_by_id.return_value = None

    with pytest.raises(UserDoesNotExistError):
        add_item_to_cart(user_repo, item_repo, user.id, new_cart_item)


def test_add_item_to_cart_when_the_item_does_not_exist(
    user_repo, item_repo, user, new_cart_item
):
    user_repo.find_user_by_id.return_value = MagicMock()
    item_repo.find_item_by_id.return_value = None

    with pytest.raises(ItemDoesNotExistError):
        add_item_to_cart(user_repo, item_repo, user.id, new_cart_item)


def test_add_item_to_cart_when_not_enough_items_in_stock(
    user_repo, item_repo, user, new_cart_item
):
    user_repo.find_user_by_id.return_value = user
    item_repo.find_item_by_id.return_value = new_cart_item

    item_to_add = ItemQuantity(
        item_id=new_cart_item.item_id, quantity=new_cart_item.quantity + 10
    )

    with pytest.raises(ItemQuantityError):
        add_item_to_cart(user_repo, item_repo, user.id, item_to_add)


def test_add_item_to_cart_when_item_already_in_cart(
    user_repo, item_repo, user, existing_cart_item
):
    user_repo.find_user_by_id.return_value = user
    item_repo.find_item_by_id.return_value = existing_cart_item

    with pytest.raises(ItemAlreadyInCartError):
        add_item_to_cart(user_repo, item_repo, user.id, existing_cart_item)


def test_add_item_to_cart(user_repo, item_repo, user, new_cart_item):
    user_repo.find_user_by_id.return_value = user
    item_repo.find_item_by_id.return_value = new_cart_item

    result = add_item_to_cart(user_repo, item_repo, user.id, new_cart_item)

    user_repo.update_user_cart_items.assert_called_once_with(user.id, new_cart_item)
    assert result == user_repo.list_items_in_cart.return_value
