
import pytest
from uuid import uuid4
import hashlib
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from be_task_ca.app import app
from be_task_ca.user.api.schema import CreateUserResponse, AddToCartResponse
from be_task_ca.user.entities.user import User
from be_task_ca.user.entities.cart_item import CartItem
from be_task_ca.user.exceptions import UserAlreadyExistsError, UserDoesNotExistError, ItemAlreadyInCartError
from be_task_ca.item.exceptions import ItemDoesNotExistError
from be_task_ca.user.api.converters import  cart_item_entity_to_dto

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_create_user(mocker):
    """Fixture used to mock create_user use case method."""

    return mocker.patch("be_task_ca.user.api.api.create_user")

@pytest.fixture
def user_request():
    """User request example"""

    return {
        "first_name": "Homer",
        "last_name": "Simpson",
        "email": "homer@simpsons.me",
        "password": "mypass",
        "shipping_address": "742 Evergreen Terrace, Springfield"
    }

@pytest.fixture
def mock_add_item_to_cart(mocker):
    """Fixture used to mock add_item_to_cart use case method."""

    return mocker.patch("be_task_ca.user.api.api.add_item_to_cart")

@pytest.fixture
def cartitem_request():
    """Cart item request example"""

    return {
        "item_id": str(uuid4()),
        "quantity": 3
    }

@pytest.fixture
def mock_list_items_in_cart(mocker):
    """Fixture used to mock mock_list_items_in_cart use case method."""

    user_id=uuid4()
    mock_cartitems = [
        CartItem(user_id=user_id, item_id=str(uuid4()), quantity=4),
        CartItem(user_id=user_id, item_id=str(uuid4()), quantity=3),
        CartItem(user_id=user_id, item_id=str(uuid4()), quantity=1),
    ]
    mock = mocker.patch("be_task_ca.user.api.api.list_items_in_cart", return_value=mock_cartitems)
    return mock

@pytest.mark.api
def test_post_user_creates_new_item(client, mock_create_user, user_request):
    """Test the 'post_user' endpoint if the user doesn't exist."""

    # Arrange
    created_user = {
        "id": uuid4(),
        "first_name": user_request["first_name"],
        "last_name": user_request["last_name"],
        "email": user_request["email"],
        "hashed_password": hashlib.sha512(
            user_request["password"].encode("UTF-8")
        ).hexdigest(),
        "shipping_address": user_request["shipping_address"]
    }

    mock_create_user.return_value = User(**created_user)
    expected_response = CreateUserResponse(**created_user)

    # Act
    response = client.post("/users", json=user_request)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    mock_create_user.assert_called_once()
    assert response.json() == jsonable_encoder(expected_response)

@pytest.mark.api
def test_post_user_already_exists(client, mock_create_user, user_request):
    """Test the 'post_user' endpoint if the user already exists."""

    # Arrange
    mock_create_user.side_effect = UserAlreadyExistsError(user_request["email"])

    # Act
    response = client.post("/users", json=user_request)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    mock_create_user.assert_called_once()
    assert response.json() == {"detail": str(UserAlreadyExistsError(user_request["email"]))}

@pytest.mark.api
def test_post_cart_adds_new_item(client, mock_add_item_to_cart, cartitem_request):
    """Test the 'post_cart' endpoint if item and user exist."""

    # Arrange
    user_id = uuid4()
    added_cartitem = {
        "user_id": user_id,
        "item_id": cartitem_request["item_id"],
        "quantity": cartitem_request["quantity"]
    }

    mock_add_item_to_cart.return_value = [CartItem(**added_cartitem)]
    expected_response = AddToCartResponse(items=[cartitem_request])

    # Act
    response = client.post(f"/users/{user_id}/cart", json=cartitem_request)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    mock_add_item_to_cart.assert_called_once()
    assert response.json() == jsonable_encoder(expected_response)

@pytest.mark.api
def test_post_cart_user_doesnt_exist(client, mock_add_item_to_cart, cartitem_request):
    """Test the 'post_cart' endpoint if user doesn'texist."""

    # Arrange
    user_id = uuid4()
    mock_add_item_to_cart.side_effect = UserDoesNotExistError()

    # Act
    response = client.post(f"/users/{user_id}/cart", json=cartitem_request)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    mock_add_item_to_cart.assert_called_once()
    assert response.json() == {"detail": str(UserDoesNotExistError())}

@pytest.mark.api
def test_post_cart_item_doesnt_exist(client, mock_add_item_to_cart, cartitem_request):
    """Test the 'post_cart' endpoint if item doesn'texist."""

    # Arrange
    user_id = uuid4()
    mock_add_item_to_cart.side_effect = ItemDoesNotExistError()

    # Act
    response = client.post(f"/users/{user_id}/cart", json=cartitem_request)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    mock_add_item_to_cart.assert_called_once()
    assert response.json() == {"detail": str(ItemDoesNotExistError())}

@pytest.mark.api
def test_post_cart_item_already_in_cart(client, mock_add_item_to_cart, cartitem_request):
    """Test the 'post_cart' endpoint if item is already in the cart."""

    # Arrange
    user_id = uuid4()
    mock_add_item_to_cart.side_effect = ItemAlreadyInCartError()

    # Act
    response = client.post(f"/users/{user_id}/cart", json=cartitem_request)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    mock_add_item_to_cart.assert_called_once()
    assert response.json() == {"detail": str(ItemAlreadyInCartError())}

@pytest.mark.api
def test_get_cart_returns_cartitems(client, mock_list_items_in_cart):
    """Test if the 'get_cart' endpoint returns a list of cart items."""

    # Arrange
    user_id = uuid4()
    expected_response = AddToCartResponse(
        items=list(map(cart_item_entity_to_dto, mock_list_items_in_cart.return_value))
    )

    # Act
    response = client.get(f"/users/{user_id}/cart")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    mock_list_items_in_cart.assert_called_once()
    assert response.json() == jsonable_encoder(expected_response)

