
import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
# from unittest.mock import Mock
from unittest import mock
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from be_task_ca.app import app
# from ....repositories.in_memory_item_repository import InMemoryItemRepository
from be_task_ca.item.api.schema import AllItemsResponse, CreateItemResponse
from be_task_ca.item.api.converters import item_entity_to_dto, item_dto_to_entity
from be_task_ca.item.repositories.item_inmemory_repository import ItemInMemoryRepository
from be_task_ca.item.entities.item import Item
from be_task_ca.item.exceptions import ItemAlreadyExistsError
### poetry run pytest -v -s --disable-warnings

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_get_all(mocker):
    """Fixture used to mock get_all use case method."""

    mock_items = [
        Item(id="f64e9eef-e576-479c-b2d2-08bb92223d79", name="Item 1", description="Description 1", price=100, quantity=10),
        Item(id="e2b03067-706b-4902-b281-97473d33007c", name="Item 2", description="Description 2", price=200, quantity=20)
    ]
    mock = mocker.patch("be_task_ca.item.api.api.get_all", return_value=mock_items)
    return mock

@pytest.fixture
def mock_create_item(mocker):
    """Fixture used to mock create_item use case method."""

    return mocker.patch("be_task_ca.item.api.api.create_item")

@pytest.mark.api
def test_get_items_returns_items(client, mock_get_all):
    """Test if the 'get_items' endpoint returns a list of items."""

    # Arrange
    expected_response = AllItemsResponse(items=list(map(item_entity_to_dto, mock_get_all.return_value)))

    # Act
    response = client.get("/items")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    mock_get_all.assert_called_once()
    assert response.json() == jsonable_encoder(expected_response)

@pytest.mark.api
def test_get_items_returns_empty_response(client, mock_get_all):
    """Test if the 'get_items' endpoint returns a list of items."""

    # Arrange
    mock_get_all.return_value = []
    expected_response = AllItemsResponse(items=list(map(item_entity_to_dto, mock_get_all.return_value)))

    # Act
    response = client.get("/items")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    mock_get_all.assert_called_once()
    assert response.json() == jsonable_encoder(expected_response)

@pytest.mark.api
def test_post_item_creates_new_item(client, mock_create_item):
    """Test the 'post_item' endpoint if the item doesn't exist."""

    # Arrange
    mock_request = {"name": "Item 1", "description": "Description 1", "price": 100, "quantity": 10}
    mock_create_item.return_value = Item(id="f64e9eef-e576-479c-b2d2-08bb92223d79", **mock_request)
    expected_response = CreateItemResponse(id="f64e9eef-e576-479c-b2d2-08bb92223d79", **mock_request)

    # Act
    response = client.post("/items", json=mock_request)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    mock_create_item.assert_called_once()
    assert response.json() == jsonable_encoder(expected_response)

@pytest.mark.api
def test_post_item_already_exists(client, mock_create_item):
    """Test the 'post_item' endpoint if the item already exists."""

    # Arrange
    mock_request = {"name": "Item 1", "description": "Description 1", "price": 100, "quantity": 10}
    mock_create_item.side_effect = ItemAlreadyExistsError(mock_request["name"])

    # Act
    response = client.post("/items", json=mock_request)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    mock_create_item.assert_called_once()
    assert response.json() == {"detail": str(ItemAlreadyExistsError(mock_request["name"]))}
