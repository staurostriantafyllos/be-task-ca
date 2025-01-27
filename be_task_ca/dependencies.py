from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db_session
from .item.repository import ItemRepo
from .user.repository import UserRepo


def get_user_repo(db: Session = Depends(get_db_session)):
    """Dependency to provide UserRepo."""
    return UserRepo(db)


def get_item_repo(db: Session = Depends(get_db_session)):
    """Dependency to provide ItemRepo."""
    return ItemRepo(db)
