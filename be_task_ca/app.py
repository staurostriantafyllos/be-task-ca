"""
NOTE:
Clean Architecture:
The instantiation of the FastAPI application, the addition of the routers and the middleware should be done in separate functions or even separate modules(the latter is more recommended). 
This follows the Single Responsibility Principle by ensuring that each part of the code has a single responsibility.

General:
There are unused variables imported inside the module, as before by using a Pylint tool,
we can easily detect such issues.
Also I have some concerns about the middleware being used here,

In this middleware, the database session is being closed after each request, 
but it's not clear if changes to the database are being committed. 
If not, you might see unexpected behavior where changes made during a request aren't persisted to the database. 
You should make sure to commit the session or rollback, in case of errors before closing it.
And of course regarding the clean architecture principles, 
you should consider injecting the database session into your route handlers and use cases using FastAPI's dependency injection system, 
rather than setting it directly on the request state. 
This would make the dependency on the database session more explicit and potentially easier to manage and test,
Also, in a highly concurrent environment, you might run into issues where a database session is shared between requests. 
SQLAlchemy sessions are not designed to be thread-safe. 
I see that we are using an async web server like Uvicorn(from the scripts at least), 
we should make sure that we're using an appropriate strategy to manage database sessions in a way that they're not shared across requests.

"""

from fastapi import FastAPI, Request, Response
from .user.api import user_router
from .item.api import item_router
from be_task_ca.user import model

from .database import SessionLocal, engine


app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon
