"""
NOTE:
Similar principles as user usecases would apply here as well. 
If there are use cases in this module that directly interact with the database or the web framework,
those responsibilities should be delegated to the appropriate layers. 
Use cases in this module should focus only on the business operations related to items.
"""

from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .model import Item
from .repository import find_item_by_name, get_all_items, save_item
from .schema import AllItemsRepsonse, CreateItemRequest, CreateItemResponse


def create_item(item: CreateItemRequest, db: Session) -> CreateItemResponse:
    search_result = find_item_by_name(item.name, db)
    if search_result is not None:
        raise HTTPException(
            status_code=409, detail="An item with this name already exists"
        )

    new_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    save_item(new_item, db)
    return model_to_schema(new_item)


def get_all(db: Session) -> List[CreateItemResponse]:
    item_list = get_all_items(db)
    return AllItemsRepsonse(items=list(map(model_to_schema, item_list)))


def model_to_schema(item: Item) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
