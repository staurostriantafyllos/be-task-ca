from typing import List

from .schema import ItemBase, Item

from ..exceptions import ItemAlreadyExistsError
from ..item.repository import ItemRepo


def create_item(item_repo: ItemRepo, item: ItemBase) -> Item:
    search_result = item_repo.find_item_by_name(item.name)
    if search_result is not None:
        raise ItemAlreadyExistsError("An item with this name already exists")

    return item_repo.save_item(item)


def get_all(item_repo: ItemRepo) -> List[Item]:
    return item_repo.get_all_items()
