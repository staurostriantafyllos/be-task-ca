import pytest
import hashlib
from uuid import UUID, uuid4
from be_task_ca.user.entities.user import User, CartItem
from be_task_ca.user.repositories.user_inmemory_repository import UserInMemoryRepository

@pytest.fixture
def repo():
    """Fixture to initialize the repository."""

    repo = UserInMemoryRepository()
    repo.users.clear()
    repo.cart_items.clear()
    return repo

@pytest.fixture
def user_to_be_created():
    """Example of user object to be created"""

    return User(
        first_name="Homer",
        last_name="Simpson",
        email="homer@simpsons.me",
        hashed_password=hashlib.sha512("password".encode("UTF-8")).hexdigest(),
        shipping_address="742 Evergreen Terrace, Springfield"
    )

@pytest.fixture
def cartitem_to_be_created():
    """Example of CartItem object to be created"""

    return CartItem(
        user_id=uuid4(),
        item_id=uuid4(),
        quantity=5
    )

@pytest.mark.repository
def test_save_user(repo, user_to_be_created):
    """Test saving a new user in the repository."""

    # Act
    saved_user = repo.save_user(user_to_be_created)
    user = repo.find_user_by_email(user_to_be_created.email)

    # Assert
    assert saved_user.id is not None
    assert type(saved_user.id)==UUID
    assert saved_user.first_name == user.first_name
    assert saved_user.last_name == user.last_name
    assert saved_user.email == user.email
    assert saved_user.hashed_password == user.hashed_password
    assert saved_user.shipping_address == user.shipping_address

@pytest.mark.repository
def test_find_user_by_email_found(repo, user_to_be_created):
    """Test finding a user by its email in the repository."""

    # Arrange
    repo.save_user(user_to_be_created)

    # Act
    user = repo.find_user_by_email(user_to_be_created.email)

    # Assert
    assert user is not None
    assert user.email == user_to_be_created.email
    assert user.first_name == user_to_be_created.first_name
    assert user.last_name == user_to_be_created.last_name

@pytest.mark.repository
def test_find_user_by_email__not_found(repo):
    """Test finding a user by email that doesn't exist."""

    # Act
    user = repo.find_user_by_email(uuid4())

    # Assert
    assert user is None

@pytest.mark.repository
def test_find_user_by_id_found(repo, user_to_be_created):
    """Test finding a user by its ID in the repository."""

    # Arrange
    new_user = repo.save_user(user_to_be_created)

    # Act
    user = repo.find_user_by_id(new_user.id)

    # Assert
    assert user is not None
    assert user.email == user_to_be_created.email
    assert user.first_name == user_to_be_created.first_name
    assert user.last_name == user_to_be_created.last_name

@pytest.mark.repository
def test_find_user_by_id_not_found(repo):
    """Test finding a user by ID that doesn't exist."""

    # Act
    user = repo.find_user_by_id(uuid4())

    # Assert
    assert user is None

@pytest.mark.repository
def test_save_cart_item(repo, cartitem_to_be_created):
    """Test saving a new cart item in the repository."""

    # Act
    saved_cart_item = repo.save_cart_item(cartitem_to_be_created)
    cart_items = repo.find_cart_items_for_user_id(cartitem_to_be_created.user_id)

    # Assert
    assert len(cart_items) == 1
    assert saved_cart_item.user_id == cart_items[0].user_id
    assert saved_cart_item.item_id == cart_items[0].item_id
    assert saved_cart_item.quantity == cart_items[0].quantity

@pytest.mark.repository
def test_find_cart_items_for_user_id(repo):
    """Test getting all cart items by user from the repository."""

    # Arrange
    user_id1=uuid4()
    user_id2=uuid4()
    cart_items = [
        CartItem(user_id=user_id1, item_id=uuid4(), quantity=10),
        CartItem(user_id=user_id1, item_id=uuid4(), quantity=20),
        CartItem(user_id=user_id1, item_id=uuid4(), quantity=30),
        CartItem(user_id=user_id2, item_id=uuid4(), quantity=40),
    ]
    for cart_item in cart_items:
        repo.save_cart_item(cart_item)

    # Act
    cart_items_user1 = repo.find_cart_items_for_user_id(user_id1)
    cart_items_user2 = repo.find_cart_items_for_user_id(user_id2)

    # Assert
    assert len(cart_items_user1) == 3
    assert len(cart_items_user2) == 1
    assert sum([c.quantity for c in cart_items_user1]) == 60
    assert cart_items_user2[0].quantity == 40
