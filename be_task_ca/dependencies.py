from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db_session
from .item.repository import ItemRepoSA
from .user.repository import UserRepoSA


def get_user_repo(db: Session = Depends(get_db_session)):
    """Dependency to provide UserRepo."""
    return UserRepoSA(db)


def get_item_repo(db: Session = Depends(get_db_session)):
    """Dependency to provide ItemRepo."""
    return ItemRepoSA(db)
