from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import DatabaseSettings

engine = None
SessionLocal = None

Base = declarative_base()


def get_db_engine():
    global engine
    if not engine:
        database_config = DatabaseSettings()
        engine = create_engine(database_config.CONNECTION_STRING)

    return engine


def get_db_session():
    database_config = DatabaseSettings()

    global SessionLocal
    if not SessionLocal:
        SessionLocal = sessionmaker(
            autocommit=database_config.AUTOCOMMIT,
            autoflush=database_config.AUTOFLUSH,
            bind=get_db_engine(),
        )

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
