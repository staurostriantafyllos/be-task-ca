from typing import List
from ..entities.item import Item
from ..interfaces.item_repository_interface import ItemRepositoryInterface
from ..exceptions import ItemAlreadyExistsError

def create_item(item: Item, repo: ItemRepositoryInterface) -> Item:
    """Create a new item if it doesn't exist in the repository."""

    if repo.find_item_by_name(item.name):
        raise ItemAlreadyExistsError(item.name) # Adding a generic exception to avoid coupling with the framework (HTTPException)
    return repo.save_item(item)

def get_all(repo: ItemRepositoryInterface) -> List[Item]:
    """Returns all items in the repository."""

    item_list = repo.get_all_items()
    return item_list