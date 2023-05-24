"""
NOTE:
Clean Architecture: 
The use cases should only contain the business logic. 
They should not be aware of the details of the data persistence layer or the web framework being used.
For example, the use case should not be directly interacting with FastAPI-specific request or response objects. 
Instead, these details should be handled at the controller layer.
Or as another example Here, the create_user use case is aware of the data persistence layer because it directly interacts with the SQLAlchemy session object.
This should be avoided. Instead, the responsibility of interacting with the database should be delegated to the repository layer. 

The refactored code might look something like this:

def create_user(user_repository, user_details):
    hashed_password = bcrypt.hashpw(user_details.password, bcrypt.gensalt())
    user = User(username=user_details.username, password=hashed_password)
    user_repository.save(user)

In general, to avoid direct dependency of use cases on SQLAlchemy models, we can introduce DTOs. 
Use Cases would interact with these DTOs instead of directly interacting with database models.

General: 
Hashing password logic inside create_user function seems a bit out of place. 
We might want to create a separate utility function for password hashing and by adding salt to the hash,
we can make the user data more secure.
Also the create_user is redefined from the outer scope, we'd can detect such common issues by installing 
tools like Pylint which makes it quite easy to figure out issues like this.
"""


import hashlib

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..item.model import Item
from ..item.repository import find_item_by_id
from .model import CartItem, User
from .repository import (
    find_cart_items_for_user_id,
    find_user_by_email,
    find_user_by_id,
    save_user,
)
from .schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)


def create_user(create_user: CreateUserRequest, db: Session) -> CreateUserResponse:
    search_result = find_user_by_email(create_user.email, db)
    if search_result is not None:
        raise HTTPException(
            status_code=409, detail="An user with this email adress already exists"
        )

    new_user = User(
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        email=create_user.email,
        hashed_password=hashlib.sha512(
            create_user.password.encode("UTF-8")
        ).hexdigest(),
        shipping_address=create_user.shipping_address,
    )

    save_user(new_user, db)

    return CreateUserResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        shipping_address=new_user.shipping_address,
    )


def add_item_to_cart(
    user_id: int, cart_item: AddToCartRequest, db: Session
) -> AddToCartResponse:
    user: User = find_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    item: Item = find_item_by_id(cart_item.item_id, db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item does not exist")
    if item.quantity < cart_item.quantity:
        raise HTTPException(status_code=409, detail="Not enough items in stock")

    item_ids = [o.item_id for o in user.cart_items]
    if cart_item.item_id in item_ids:
        raise HTTPException(status_code=409, detail="Item already in cart")

    new_cart_item: CartItem = CartItem(
        user_id=user.id, item_id=cart_item.item_id, quantity=cart_item.quantity
    )

    user.cart_items.append(new_cart_item)

    save_user(user, db)

    return list_items_in_cart(user.id, db)


def list_items_in_cart(user_id, db):
    cart_items = find_cart_items_for_user_id(user_id, db)
    return AddToCartResponse(items=list(map(cart_item_model_to_schema, cart_items)))


def cart_item_model_to_schema(model: CartItem):
    return AddToCartRequest(item_id=model.item_id, quantity=model.quantity)
