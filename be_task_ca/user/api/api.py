from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .converters import user_entity_to_dto, user_dto_to_entity, cart_item_dto_to_entity, cart_item_entity_to_dto
from ..repositories.user_postgres_repository import UserPostgresRepository
from ..repositories.user_inmemory_repository import UserInMemoryRepository
from ..interfaces.user_repository_interface import UserRepositoryInterface
from ..api.schema import CreateUserRequest, CreateUserResponse, AddToCartRequest, AddToCartResponse
from ...common import get_db
from ..exceptions import UserAlreadyExistsError, UserDoesNotExistError, ItemAlreadyInCartError
from ..use_cases.usecases import create_user, add_item_to_cart, list_items_in_cart
from ...item.repositories.item_postgres_repository import ItemPostgresRepository
from ...item.repositories.item_inmemory_repository import ItemInMemoryRepository
from ...item.interfaces.item_repository_interface import ItemRepositoryInterface
from ...item.exceptions import ItemDoesNotExistError
from ...item.api.api import get_item_inmemory_repository


user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)

def get_user_postgres_repository(db: Session = Depends(get_db)) -> UserRepositoryInterface:
    """Retrieves a user postgres repository dependency"""

    return UserPostgresRepository(db)

def get_user_inmemory_repository() -> UserRepositoryInterface:
    """Retrieves a user in-memory repository dependency"""

    return UserInMemoryRepository()

@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_user(
    dto_user: CreateUserRequest,
    repo: UserRepositoryInterface = Depends(get_user_inmemory_repository)
) -> CreateUserResponse:
    """Handles the creation of a new user."""

    user = user_dto_to_entity(dto_user)
    try:
        user = create_user(user, repo)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    dto_user = user_entity_to_dto(user)
    return dto_user

@user_router.post("/{user_id}/cart", status_code=status.HTTP_201_CREATED)
async def post_cart(
    user_id: UUID, cart_item_dto: AddToCartRequest,
    user_repo: UserRepositoryInterface = Depends(get_user_inmemory_repository),
    item_repo: ItemRepositoryInterface = Depends(get_item_inmemory_repository)
) -> AddToCartResponse:
    """Adds an item to the user's cart."""

    cart_item = cart_item_dto_to_entity(cart_item_dto, user_id)
    try:
        cart_items = add_item_to_cart(cart_item, user_repo, item_repo)
    except (UserDoesNotExistError, ItemDoesNotExistError, ItemAlreadyInCartError) as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return AddToCartResponse(items=list(map(cart_item_entity_to_dto, cart_items)))


@user_router.get("/{user_id}/cart", status_code=status.HTTP_200_OK)
async def get_cart(
    user_id: UUID,
    repo: UserRepositoryInterface = Depends(get_user_inmemory_repository)
) -> AddToCartResponse:
    """Retrieves all items in the user's cart."""

    cart_items = list_items_in_cart(user_id, repo)

    return AddToCartResponse(items=list(map(cart_item_entity_to_dto, cart_items)))
