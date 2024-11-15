from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .usecases import create_item, get_all

from ..common import get_db

from .schema import CreateItemRequest, CreateItemResponse, AllItemsResponse
from .repository import ItemPostgresRepository
from .domain import Item
from .exceptions import ItemAlreadyExistsError

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)

@item_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_item(
    dto_item: CreateItemRequest, db: Session = Depends(get_db)
) -> CreateItemResponse:
    item = dto_to_entity(dto_item)

    repo = ItemPostgresRepository(db) #TODO: Inyectar el repo con Depends????
    try:
        item = create_item(dto_item, repo)
    except ItemAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    dto_item = entity_to_dto(item)
    return dto_item

@item_router.get("/", status_code=status.HTTP_200_OK)
async def get_items(db: Session = Depends(get_db)) -> AllItemsResponse:
    """???"""
    repo = ItemPostgresRepository(db) #TODO: Inyectar el repo con Depends????
    item_list = get_all(repo)

    # Converting domain items to DTO
    dto_list=list(map(entity_to_dto, item_list))
    print(dto_list)
    return AllItemsResponse(items=dto_list)

def entity_to_dto(item: Item) -> CreateItemResponse:
    """???"""
    # TODO: Dónde ubico este transformador/converter?
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

def dto_to_entity(dto_item: CreateItemResponse) -> Item:
    """???"""
    # TODO: Dónde ubico este transformador/converter?
    return Item(
        name=dto_item.name,
        description=dto_item.description,
        price=dto_item.price,
        quantity=dto_item.quantity,
    )
