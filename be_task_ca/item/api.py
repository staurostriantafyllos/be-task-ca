"""
NOTE:

The actual logic of the endpoint should not be in the API module. Rather, this logic should be moved to a use case or service.
Also the formatting of the imports are not pythonic, in Python the way we do imports are as follow:

import builtins
# space
import third party or community libraries
# space
import internal modules in the following way:
from some import Some
# no space
from .some import Some
# no space
from ..some import Some
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .usecases import create_item, get_all

from ..common import get_db

from .schema import CreateItemRequest, CreateItemResponse


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest, db: Session = Depends(get_db)
) -> CreateItemResponse:
    return create_item(item, db)


@item_router.get("/")
async def get_items(db: Session = Depends(get_db)):
    return get_all(db)
