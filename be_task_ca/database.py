"""
NOTE:
Clean Architecture: 
Separate the engine creation and the session management to make the design more modular.
These functions could be placed in a factory or provider module that could be responsible for creating and managing database related objects.
Also, the system uses a single centralized database. 
This is counter to the typical microservices architecture where each service usually has its own database to ensure loose coupling. 

General: 
You could use a context manager for handling the database sessions. 
This would ensure that your sessions are correctly handled even in cases where exceptions occur.
Similiar to what we discussed during the meeting :)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:example@localhost:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
