from typing import List
from .domain import Item
from .interfaces import ItemRepositoryInterface
from .exceptions import ItemAlreadyExistsError

def create_item(item: Item, repo: ItemRepositoryInterface) -> Item:
    """
    Create a new item if it doesn't exist in the repository.
    """

    if repo.find_item_by_name(item.name):
        raise ItemAlreadyExistsError(item.name) # Adding a generic exception to avoid coupling with the framework (HTTPException)
    return repo.save_item(item)

def get_all(repo: ItemRepositoryInterface) -> List[Item]:
    """???"""
    item_list = repo.get_all_items()
    return item_list