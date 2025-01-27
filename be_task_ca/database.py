from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DatabaseSettings

engine = None
SessionLocal = None

Base = declarative_base()


def get_db_session():

    database_config = DatabaseSettings()

    global engine, SessionLocal
    if not engine:
        engine = create_engine(database_config.CONNECTION_STRING)

    if not SessionLocal:
        SessionLocal = sessionmaker(
            autocommit=database_config.AUTOCOMMIT,
            autoflush=database_config.AUTOFLUSH,
            bind=engine,
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
