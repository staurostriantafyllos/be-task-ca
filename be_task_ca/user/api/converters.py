import hashlib
from uuid import UUID
from ..entities.user import User
from ..entities.cart_item import CartItem
from ..api.schema import CreateUserResponse, AddToCartRequest

def user_entity_to_dto(user: User) -> CreateUserResponse:
    """Converts a domain entity to a DTO."""
    return CreateUserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        shipping_address=user.shipping_address
    )


def user_dto_to_entity(dto_user: CreateUserResponse) -> User:
    """Converts a DTO to a domain entity."""
    return User(
        first_name=dto_user.first_name,
        last_name=dto_user.last_name,
        email=dto_user.email,
        hashed_password=hashlib.sha512(
            dto_user.password.encode("UTF-8")
        ).hexdigest(),
        shipping_address=dto_user.shipping_address,
    )

def cart_item_dto_to_entity(cart_item_dto: AddToCartRequest, user_id:UUID) -> CartItem:
    """Converts a DTO to a domain entity."""
    return CartItem(
        user_id=user_id,
        item_id=cart_item_dto.item_id,
        quantity=cart_item_dto.quantity
    )

def cart_item_entity_to_dto(cart_item: CartItem) -> AddToCartRequest:
    """Converts a domain entity to a DTO."""
    return AddToCartRequest(
        item_id=cart_item.item_id,
        quantity=cart_item.quantity
    )