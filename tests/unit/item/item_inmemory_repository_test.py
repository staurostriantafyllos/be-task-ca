import pytest
from uuid import UUID, uuid4
from be_task_ca.item.use_cases.usecases import get_all, create_item
from be_task_ca.item.entities.item import Item
from be_task_ca.item.exceptions import ItemAlreadyExistsError
from be_task_ca.item.repositories.item_inmemory_repository import ItemInMemoryRepository

@pytest.fixture
def repo():
    """Fixture to initialize the repository."""

    repo = ItemInMemoryRepository()
    repo.items.clear() # Cleaning items before executing each test
    return repo

@pytest.mark.repository
def test_save_item(repo):
    """Test saving a new item in the repository."""

    # Arrange
    new_item = Item(id=None, name="Item 1", description="Description 1", price=100, quantity=10)

    # Act
    saved_item = repo.save_item(new_item)
    items = repo.get_all_items()

    # Assert
    assert saved_item.id is not None
    assert type(saved_item.id)==UUID
    assert saved_item.name == new_item.name
    assert saved_item.description == new_item.description
    assert saved_item.price == new_item.price
    assert saved_item.quantity == new_item.quantity
    assert len(items) == 1
    assert items[0].name == "Item 1"

@pytest.mark.repository
def test_get_all_items(repo):
    """Test getting all items from the repository."""

    # Arrange
    new_items = [
        Item(id=None, name="Item 1", description="Description 1", price=100, quantity=10),
        Item(id=None, name="Item 2", description="Description 2", price=200, quantity=20)
    ]
    for new_item in new_items:
        repo.save_item(new_item)

    # Act
    items = repo.get_all_items()

    # Assert
    assert len(items) == 2
    assert items[0].name == "Item 1"
    assert items[1].name == "Item 2"

@pytest.mark.repository
def test_find_item_by_name_found(repo):
    """Test finding an item by its name in the repository."""

    # Arrange
    item_to_be_created = Item(id=None, name="Item 1", description="Description 1", price=100, quantity=10)
    repo.save_item(item_to_be_created)

    # Act
    item = repo.find_item_by_name("Item 1")

    # Assert
    assert item is not None
    assert item.name == "Item 1"
    assert item.description == "Description 1"

@pytest.mark.repository
def test_find_item_by_name_not_found(repo):
    """Test finding an item by name that doesn't exist."""

    # Act
    item = repo.find_item_by_name("Item 1")

    # Assert
    assert item is None

@pytest.mark.repository
def test_find_item_by_id_found(repo):
    """Test finding an item by its ID in the repository."""

    # Arrange
    item_to_be_created = Item(id=None, name="Item 1", description="Description 1", price=100, quantity=10)
    saved_item = repo.save_item(item_to_be_created)

    # Act
    item = repo.find_item_by_id(saved_item.id)

    # Assert
    assert item is not None
    assert item.id == saved_item.id
    assert item.name == "Item 1"
    assert item.description == "Description 1"

@pytest.mark.repository
def test_find_item_by_id_not_found(repo):
    """Test finding an item by ID that doesn't exist."""

    # Act
    item = repo.find_item_by_id(uuid4())

    # Assert
    assert item is None
