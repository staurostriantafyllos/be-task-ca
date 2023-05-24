"""
NOTE:

Ideally, the creation of the database schema should be done in a separate module or a script that is solely responsible for setting up your application. 
This could be a script that is run when your application is deployed. Or it can be done within dockerization process

"""

from .database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from .user import model1
from .item import model2


def create_db_schema():
    Base.metadata.create_all(bind=engine)
