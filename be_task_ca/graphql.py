import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import Depends

from be_task_ca.dependencies import get_item_repo
from be_task_ca.item.graph import ItemQuery
from be_task_ca.item.repository import ItemRepo


async def get_context(item_repo: ItemRepo = Depends(get_item_repo)):  # noqa: B008
    """
    Prepare the dependencies for the GraphQL context.
    """
    return {"item_repo": item_repo}


@strawberry.type
class Query(
    ItemQuery,
):
    """
    Query that merges all the queries from the different modules.
    """

    pass


graphql_router = GraphQLRouter(
    schema=strawberry.Schema(query=Query),
    context_getter=get_context,
)
