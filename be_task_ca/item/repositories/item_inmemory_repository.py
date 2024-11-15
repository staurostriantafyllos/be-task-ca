# from typing import List, Optional
# from uuid import UUID
# from .model import Item as ItemModel
# from ..entities.items import Item
# from ..interfaces.item_repository_interface import ItemRepositoryInterface

# class ItemInMemoryRepository(ItemRepositoryInterface):
#     """???"""

#     def __init__(self):
#         pass

#     def get_all_items(self) -> List[Item]:
#         """Retrieves all items"""
#         # item_list = self.db_session.query(ItemModel).all()
#         # return list(map(self._model_to_entity, item_list))
#         pass

#     def find_item_by_name(self, name: str) -> Optional[Item]:
#         """???"""

#         # item_model = self.db_session.query(ItemModel).filter(ItemModel.name == name).first()

#         # if item_model is None:
#         #     return None

#         # return self._model_to_entity(item_model)
#         pass

#     def find_item_by_id(self, id: UUID) -> Item:
#         """???"""

#         # item_model = self.db_session.query(ItemModel).filter(ItemModel.id == id).first()

#         # if item_model is None:
#         #     return None

#         # return self._model_to_entity(item_model)
#         pass

#     def save_item(self, item: Item) -> Item:
#         """???"""

#         # item_model = self._entity_to_model(item)

#         # self.db_session.add(item_model)
#         # self.db_session.commit()
#         # self.db_session.refresh(item_model)

#         # print(item_model)

#         # return self._model_to_entity(item_model)
#         pass

#     # def _model_to_entity(self, item: ItemModel) -> Item:
#     #     return Item(
#     #         id=item.id,
#     #         name=item.name,
#     #         description=item.description,
#     #         price=item.price,
#     #         quantity=item.quantity,
#     #     )

#     # def _entity_to_model(self, item: Item) -> ItemModel:
#     #     return ItemModel(
#     #         name=item.name,
#     #         description=item.description,
#     #         price=item.price,
#     #         quantity=item.quantity,
#     #     )