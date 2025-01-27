from typing import List
from uuid import UUID

from .schema import ItemBase, Item as ItemSchema
from .model import Item


class ItemRepo:
    def __init__(self, db):
        self.db = db

    def save_item(self, item: ItemBase) -> ItemSchema:
        new_item = Item(
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )

        self.db.add(new_item)
        self.db.commit()

        return ItemSchema.model_validate(new_item)

    def get_all_items(self) -> List[ItemSchema]:
        items = self.db.query(Item).all()
        return [ItemSchema.model_validate(item) for item in items]

    def find_item_by_name(self, name: str) -> ItemSchema | None:
        item = self.db.query(Item).filter(Item.name == name).first()
        if not item:
            return
        return ItemSchema.model_validate(item)

    def find_item_by_id(self, id: UUID) -> ItemSchema | None:
        item = self.db.query(Item).filter(Item.id == id).first()
        if not item:
            return
        return ItemSchema.model_validate(item)
