from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from .repository import UserRepo
from .schema import ItemQuantity, AddToCartResponse, UserPrivate
from .usecases import add_item_to_cart, create_user, list_items_in_cart

from ..dependencies import get_item_repo, get_user_repo
from ..exceptions import (
    ItemAlreadyInCartError,
    ItemDoesNotExistError,
    ItemQuantityError,
    UserAlreadyExistsError,
    UserDoesNotExistError,
)
from ..item.repository import ItemRepo


user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@user_router.post("/")
async def post_customer(
    user: UserPrivate, user_repo: UserRepo = Depends(get_user_repo)
):
    try:
        return create_user(user_repo, user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID,
    cart_item: ItemQuantity,
    user_repo: UserRepo = Depends(get_user_repo),
    item_repo: ItemRepo = Depends(get_item_repo),
) -> AddToCartResponse:
    try:
        cart_items = add_item_to_cart(user_repo, item_repo, user_id, cart_item)
        return AddToCartResponse(items=cart_items)
    except UserDoesNotExistError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ItemDoesNotExistError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ItemQuantityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except ItemAlreadyInCartError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@user_router.get("/{user_id}/cart")
async def get_cart(
    user_id: UUID, user_repo: UserRepo = Depends(get_user_repo)
) -> AddToCartResponse:
    try:
        cart_items = list_items_in_cart(user_repo, user_id)
        return AddToCartResponse(items=cart_items)
    except UserDoesNotExistError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
