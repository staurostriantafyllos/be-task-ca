from ..api.schema import CreateItemResponse
from ..entities.item import Item

def item_entity_to_dto(item: Item) -> CreateItemResponse:
    """Converts a domain entity to a DTO."""
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

def item_dto_to_entity(dto_item: CreateItemResponse) -> Item:
    """Converts a DTO to a domain entity."""
    return Item(
        name=dto_item.name,
        description=dto_item.description,
        price=dto_item.price,
        quantity=dto_item.quantity,
    )