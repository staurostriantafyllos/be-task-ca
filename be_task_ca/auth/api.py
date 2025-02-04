from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from be_task_ca.auth.repository import (
    create_user,
    login_user,
    refresh_token,
)
from be_task_ca.auth.schema import (
    RefreshRequest,
    TokenResponse,
    UserCredentials,
    UserSignup,
)
from be_task_ca.exceptions import (
    UserException,
    UserLoginError,
    UserSignupError,
    UserTokenRefreshException,
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/signup")
async def signup(user: UserSignup):
    try:
        status_code = await create_user(user)
    except UserSignupError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except UserException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    return JSONResponse(status_code=status_code, content={"message": "User created"})


@auth_router.post("/login", response_model=TokenResponse)
async def login(credentials: UserCredentials):
    try:
        status_code, data = await login_user(credentials)
    except UserLoginError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    return JSONResponse(status_code=status_code, content=data)


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest):
    try:
        status_code, data = await refresh_token(request.refresh_token)
    except UserTokenRefreshException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    return JSONResponse(status_code=status_code, content=data)
