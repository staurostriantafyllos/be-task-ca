from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from be_task_ca.auth.repository import authenticate_token
from be_task_ca.exceptions import (
    TokenExpiredError,
    TokenInvalidError,
    TokenMalformedError,
)
from .database import get_db_session
from .item.repository import ItemRepoSA
from .user.repository import UserRepoSA


def get_user_repo(db: Session = Depends(get_db_session)):  # noqa: B008
    """Dependency to provide UserRepo."""
    return UserRepoSA(db)


def get_item_repo(db: Session = Depends(get_db_session)):  # noqa: B008
    """Dependency to provide ItemRepo."""
    return ItemRepoSA(db)


def get_logged_user(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),  # noqa: B008
) -> dict:
    token = credentials.credentials
    try:
        payload = authenticate_token(token)
    except (TokenExpiredError, TokenMalformedError, TokenInvalidError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return payload
