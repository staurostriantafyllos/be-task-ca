import pytest
import hashlib
from uuid import uuid4
from be_task_ca.user.use_cases.usecases import create_user
from be_task_ca.item.entities.item import Item
from be_task_ca.user.entities.user import User
from be_task_ca.user.entities.cart_item import CartItem
from be_task_ca.user.exceptions import UserAlreadyExistsError, UserDoesNotExistError, ItemAlreadyInCartError
from be_task_ca.item.exceptions import ItemDoesNotExistError
from be_task_ca.user.use_cases.usecases import list_items_in_cart, add_item_to_cart

@pytest.fixture
def user_mock_repo(mocker):
    """Fixture to mock the User repository."""
    return mocker.Mock()

@pytest.fixture
def item_mock_repo(mocker):
    """Fixture to mock the item repository."""
    return mocker.Mock()


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
def cartitem_to_be_added():
    """Example of cart item object to be added"""

    return CartItem(
        user_id=uuid4(),
        item_id=uuid4(),
        quantity=5
    )

@pytest.mark.usecases
def test_create_user_creates_new_user(user_mock_repo, user_to_be_created):
    """Tests the use case 'create_user' when user doesn't exist."""

    # Arrange
    user_mock_repo.find_user_by_email.return_value = None # User doesn't exist
    user_mock_repo.save_user.return_value = user_to_be_created
    user_mock_repo.save_user.return_value.id = uuid4()

    # Act
    created_user = create_user(user_to_be_created, user_mock_repo)

    # Assert
    assert created_user == user_mock_repo.save_user.return_value
    user_mock_repo.save_user.assert_called_once_with(user_to_be_created)
    user_mock_repo.find_user_by_email.assert_called_once_with(user_to_be_created.email)

@pytest.mark.usecases
def test_create_user_already_exists(user_mock_repo, user_to_be_created):
    """Tests the use case 'create_user' when user already exists."""

    # Arrange
    existing_user = user_to_be_created
    existing_user.id = uuid4()
    user_mock_repo.find_user_by_email.return_value = existing_user

    # Act
    with pytest.raises(UserAlreadyExistsError) as e:
        create_user(user_to_be_created, user_mock_repo)

    # Assert
    assert str(e.value) == str(UserAlreadyExistsError(user_to_be_created.email))
    user_mock_repo.find_user_by_email.assert_called_once_with(user_to_be_created.email)
    user_mock_repo.save_user.assert_not_called()

@pytest.mark.usecases
def test_list_items_in_cart(user_mock_repo):
    """Tests if the use case 'list_items_in_cart' returns a list of cart items."""

    # Arrange
    user_id=uuid4()
    mock_cartitems = [
        CartItem(user_id=user_id, item_id=str(uuid4()), quantity=4),
        CartItem(user_id=user_id, item_id=str(uuid4()), quantity=3),
        CartItem(user_id=user_id, item_id=str(uuid4()), quantity=1),
    ]
    user_mock_repo.find_cart_items_for_user_id.return_value = mock_cartitems

    # Act
    cart_items = list_items_in_cart(user_id, user_mock_repo)

    # Assert
    assert cart_items == mock_cartitems
    user_mock_repo.find_cart_items_for_user_id.assert_called_once()

@pytest.mark.usecases
def test_add_item_to_cart_adds_new_item(
        user_mock_repo, item_mock_repo, cartitem_to_be_added, user_to_be_created
):
    """Tests the use case 'add_item_to_cart'."""

    # Arrange
    user_mock_repo.find_user_by_id.return_value = user_to_be_created
    user_mock_repo.find_user_by_id.return_value.id = uuid4()
    user_mock_repo.find_user_by_id.return_value.cart_items = []
    item_mock_repo.find_item_by_id.return_value = Item(
        id=uuid4(), name="Item 1", description="Description 1", price=100, quantity=10
    )
    user_mock_repo.save_cart_item.return_value = cartitem_to_be_added
    user_mock_repo.find_cart_items_for_user_id.return_value=[]

    # Act
    user_cartitems = add_item_to_cart(cartitem_to_be_added, user_mock_repo, item_mock_repo)

    # Assert
    assert user_cartitems == user_mock_repo.find_cart_items_for_user_id.return_value
    user_mock_repo.find_user_by_id.assert_called_once_with(cartitem_to_be_added.user_id)
    item_mock_repo.find_item_by_id.assert_called_once_with(cartitem_to_be_added.item_id)
    user_mock_repo.save_cart_item.assert_called_once_with(cartitem_to_be_added)
    user_mock_repo.find_cart_items_for_user_id.assert_called_once()

@pytest.mark.usecases
def test_add_item_to_cart_when_user_doesnt_exist(
        user_mock_repo, item_mock_repo, cartitem_to_be_added, user_to_be_created
):
    """Tests the use case 'add_item_to_cart' when user doesn't exist."""

    # Arrange
    user_mock_repo.find_user_by_id.side_effect = UserDoesNotExistError()

    # Act
    with pytest.raises(UserDoesNotExistError) as e:
        add_item_to_cart(cartitem_to_be_added, user_mock_repo, item_mock_repo)

    # Assert
    assert str(e.value) == str(UserDoesNotExistError())
    user_mock_repo.find_user_by_id.assert_called_once_with(cartitem_to_be_added.user_id)
    user_mock_repo.save_cart_item.assert_not_called()

@pytest.mark.usecases
def test_add_item_to_cart_when_item_doesnt_exist(
        user_mock_repo, item_mock_repo, cartitem_to_be_added, user_to_be_created
):
    """Tests the use case 'add_item_to_cart' when item doesn't exist."""

    # Arrange
    user_mock_repo.find_user_by_id.return_value = user_to_be_created
    user_mock_repo.find_user_by_id.return_value.id = uuid4()
    item_mock_repo.find_item_by_id.side_effect = ItemDoesNotExistError()

    # Act
    with pytest.raises(ItemDoesNotExistError) as e:
        add_item_to_cart(cartitem_to_be_added, user_mock_repo, item_mock_repo)

    # Assert
    assert str(e.value) == str(ItemDoesNotExistError())
    user_mock_repo.find_user_by_id.assert_called_once_with(cartitem_to_be_added.user_id)
    item_mock_repo.find_item_by_id.assert_called_once_with(cartitem_to_be_added.item_id)
    user_mock_repo.save_cart_item.assert_not_called()

@pytest.mark.usecases
def test_add_item_to_cart_when_item_already_in_cart(
        user_mock_repo, item_mock_repo, cartitem_to_be_added, user_to_be_created
):
    """Tests the use case 'add_item_to_cart' when item was already added."""

    # Arrange
    user_mock_repo.find_user_by_id.return_value = user_to_be_created
    user_mock_repo.find_user_by_id.return_value.id = uuid4()
    user_mock_repo.find_user_by_id.return_value.cart_items = [{
        "item_id": cartitem_to_be_added.item_id
    }]
    item_mock_repo.find_item_by_id.return_value = Item(
        id=uuid4(), name="Item 1", description="Description 1", price=100, quantity=10
    )

    # Act
    with pytest.raises(ItemAlreadyInCartError) as e:
        add_item_to_cart(cartitem_to_be_added, user_mock_repo, item_mock_repo)

    # Assert
    assert str(e.value) == str(ItemAlreadyInCartError())
    user_mock_repo.save_cart_item.assert_not_called()

