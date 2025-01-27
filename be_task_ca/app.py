# import logging

from fastapi import FastAPI

from .logging_config import initialise_logging
from .config import LoggingSettings

from .user.api import user_router
from .item.api import item_router


logging_settings = LoggingSettings()

initialise_logging(
    log_level=logging_settings.LEVEL_ROOT,
    sqlalchemy_level=logging_settings.LEVEL_SQLALCHEMY,
)

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)


@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon


# logger = logging.getLogger(__name__)

# @app.exception_handler(Exception)
# async def generic_exception_handler(request: Request, exc: Exception):
#     """
#     Generic exception handler for HTTP 500 errors.
#     """
#     # Log the error for debugging purposes
#     logger.error(f"Unexpected error occurred: {exc}", exc_info=True)

#     # Return a JSON response to the client
#     return Response(
#         "Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
#     )
