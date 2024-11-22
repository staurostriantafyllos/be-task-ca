import pytest
from uuid import uuid4
from be_task_ca.item.use_cases.usecases import get_all, create_item
from be_task_ca.item.entities.item import Item
from be_task_ca.item.exceptions import ItemAlreadyExistsError

@pytest.fixture
def mock_repo(mocker):
    """Fixture to mock the Item repository."""
    return mocker.Mock()

@pytest.mark.usecases
def test_create_item_creates_new_item(mock_repo):
    """Tests the use case 'create_item' when item doesn't exist."""

    # Arrange
    item_to_be_created = Item(
        id=None, name="Item 1", description="Description 1", price=100, quantity=10
    )
    mock_repo.find_item_by_name.return_value = None # Item doesn't exist
    mock_repo.save_item.return_value = item_to_be_created
    mock_repo.save_item.return_value.id = uuid4()

    # Act
    created_item = create_item(item_to_be_created, mock_repo)

    # Assert
    assert created_item == mock_repo.save_item.return_value
    mock_repo.find_item_by_name.assert_called_once_with(item_to_be_created.name)
    mock_repo.save_item.assert_called_once_with(item_to_be_created)

@pytest.mark.usecases
def test_create_item_already_exists(mock_repo):
    """Tests the use case 'create_item' when item already exists."""

    # Arrange
    item_to_be_created = Item(
        id=None, name="Item 1", description="Description 1", price=100, quantity=10
    )

    existing_item = item_to_be_created
    existing_item.id = uuid4()
    mock_repo.find_item_by_name.return_value = existing_item

    # Act
    with pytest.raises(ItemAlreadyExistsError) as e:
        create_item(item_to_be_created, mock_repo)

    # Assert
    assert str(e.value) == str(ItemAlreadyExistsError(item_to_be_created.name))
    mock_repo.find_item_by_name.assert_called_once_with(item_to_be_created.name)
    mock_repo.save_item.assert_not_called()

@pytest.mark.usecases
def test_get_all_items(mock_repo):
    """Tests if the use case 'get_all' returns a list of items."""

    # Arrange
    mock_items = [
        Item(id=uuid4(), name="Item 1", description="Description 1", price=100, quantity=10),
        Item(id=uuid4(), name="Item 2", description="Description 2", price=200, quantity=20)
    ]
    mock_repo.get_all_items.return_value = mock_items

    # Act
    items = get_all(mock_repo)

    # Assert
    assert items == mock_items
    mock_repo.get_all_items.assert_called_once()
