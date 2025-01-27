from unittest import mock
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from be_task_ca.app import app
from be_task_ca.dependencies import get_user_repo
from be_task_ca.exceptions import UserDoesNotExistError
from be_task_ca.user.repository import UserRepo
from be_task_ca.user.schema import AddToCartResponse, ItemQuantity

client = TestClient(app)


@pytest.fixture
def user_repo():
    return MagicMock(spec=UserRepo)


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def cart_items():
    return [
        ItemQuantity(item_id=uuid4(), quantity=2),
        ItemQuantity(item_id=uuid4(), quantity=1),
    ]


@mock.patch("be_task_ca.user.api.list_items_in_cart")
def test_get_users_cart(usecase_mock, user_repo, user_id, cart_items):
    usecase_mock.return_value = cart_items
    app.dependency_overrides[get_user_repo] = lambda: user_repo

    response = client.get(f"/users/{user_id}/cart")

    usecase_mock.assert_called_once_with(user_repo, user_id)
    assert response.status_code == 200
    assert response.json() == AddToCartResponse(items=cart_items).model_dump(
        mode='json'
    )

    app.dependency_overrides = {}


@mock.patch("be_task_ca.user.api.list_items_in_cart")
def test_get_unknown_users_cart(usecase_mock, user_repo, user_id):
    usecase_mock.side_effect = UserDoesNotExistError("User does not exist")
    app.dependency_overrides[get_user_repo] = lambda: user_repo

    response = client.get(f"/users/{user_id}/cart")

    usecase_mock.assert_called_once_with(user_repo, user_id)
    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}

    app.dependency_overrides = {}
