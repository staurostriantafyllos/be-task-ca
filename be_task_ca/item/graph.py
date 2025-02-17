from typing import List

import strawberry

from be_task_ca.item.schema import Item
from be_task_ca.item.usecases import get_all


@strawberry.experimental.pydantic.type(model=Item, all_fields=True)
class ItemType:
    pass


@strawberry.type
class ItemQuery:
    @strawberry.field
    async def items(self, info: strawberry.Info) -> List[ItemType]:
        item_repo = info.context.get("item_repo")
        if item_repo is None:
            raise ValueError("Item repository is missing in context")

        items = get_all(item_repo)
        return [ItemType.from_pydantic(item) for item in items]
