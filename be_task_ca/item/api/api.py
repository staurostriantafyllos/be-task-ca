from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
# from ..use_cases.usecases import create_item, get_all
from be_task_ca.item.use_cases.usecases import create_item, get_all
from ...common import get_db
from ..api.schema import CreateItemRequest, CreateItemResponse, AllItemsResponse
from ..repositories.item_postgres_repository import ItemPostgresRepository
from ..repositories.item_inmemory_repository import ItemInMemoryRepository
from ..interfaces.item_repository_interface import ItemRepositoryInterface
from ..exceptions import ItemAlreadyExistsError
from .converters import item_entity_to_dto, item_dto_to_entity

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)

def get_item_postgres_repository(db: Session = Depends(get_db)) -> ItemRepositoryInterface:
    """Retrieves an item postgres repository dependency."""

    return ItemPostgresRepository(db)

def get_item_inmemory_repository() -> ItemRepositoryInterface:
    """Retrieves an item in-memory repository dependency."""

    return ItemInMemoryRepository()

@item_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_item(
    dto_item: CreateItemRequest,
    repo: ItemRepositoryInterface = Depends(get_item_inmemory_repository)
) -> CreateItemResponse:
    """Handles the creation of a new item."""

    item = item_dto_to_entity(dto_item)

    try:
        item = create_item(item, repo)
    except ItemAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return item_entity_to_dto(item)

@item_router.get("/", status_code=status.HTTP_200_OK)
async def get_items(
    repo: ItemRepositoryInterface = Depends(get_item_inmemory_repository)
) -> AllItemsResponse:
    """Retrieves all items."""

    item_list = get_all(repo)
    return AllItemsResponse(items=list(map(item_entity_to_dto, item_list)))
