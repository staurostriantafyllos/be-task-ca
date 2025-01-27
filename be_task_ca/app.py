from fastapi import FastAPI

from .logging_config import initialise_logging
from .config import LoggingSettings

from .user.api import user_router
from .item.api import item_router


async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon


def create_app():
    logging_settings = LoggingSettings()

    initialise_logging(
        log_level=logging_settings.LEVEL_ROOT,
        sqlalchemy_level=logging_settings.LEVEL_SQLALCHEMY,
    )

    app = FastAPI()
    app.include_router(user_router)
    app.include_router(item_router)
    app.add_api_route("/", root)
    return app


app = create_app()
