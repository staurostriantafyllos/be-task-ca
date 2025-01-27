from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_item_repo
from ..exceptions import ItemAlreadyExistsError
from ..item.repository import ItemRepo

from .usecases import create_item, get_all

from .schema import AllItemsRepsonse, ItemBase, Item


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
    item: ItemBase, item_repo: ItemRepo = Depends(get_item_repo)
) -> Item:
    try:
        return create_item(item_repo, item)
    except ItemAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@item_router.get("/")
async def get_items(item_repo: ItemRepo = Depends(get_item_repo)) -> AllItemsRepsonse:
    items = get_all(item_repo)
    return AllItemsRepsonse(items=items)
