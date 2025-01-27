from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DatabaseSettings

database_config = DatabaseSettings()

engine = create_engine(database_config.CONNECTION_STRING)
SessionLocal = sessionmaker(
    autocommit=database_config.AUTOCOMMIT,
    autoflush=database_config.AUTOFLUSH,
    bind=engine,
)

Base = declarative_base()


def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
