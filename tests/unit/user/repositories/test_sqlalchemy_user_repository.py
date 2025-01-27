import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from be_task_ca.database import Base
from be_task_ca.item.model import Item  # noqa
from be_task_ca.user.model import CartItem, User  # noqa
from be_task_ca.user.repository import UserRepoSA
from be_task_ca.user.schema import UserPrivate


@pytest.fixture(scope="function")
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def user_repo(db):
    return UserRepoSA(db)


def test_save_user(user_repo, db):
    user_private = UserPrivate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password",
        shipping_address="123 Main St"
    )

    assert db.query(User).count() == 0

    user_schema = user_repo.save_user(user_private)

    assert user_schema.email == "john.doe@example.com"
    assert user_schema.first_name == "John"
    assert user_schema.last_name == "Doe"

    assert db.query(User).count() == 1


def test_find_user_by_email(user_repo, db):
    email = "john.doe@example.com"
    db.add(
        User(
            first_name="John",
            last_name="Doe",
            email=email,
            hashed_password="password",
            shipping_address="123 Main St"
        )
    )
    db.commit()

    user_schema = user_repo.find_user_by_email(email)

    assert user_schema is not None
    assert user_schema.email == email
    assert user_schema.first_name == "John"


def test_find_user_by_id(user_repo, db):
    user = User(
        first_name="John",
        last_name="Doe",
        email="",
        hashed_password="",
        shipping_address=""
    )
    db.add(user)
    db.commit()

    user_schema = user_repo.find_user_by_id(user.id)

    assert user_schema is not None
    assert user_schema.id == user.id
    assert user_schema.first_name == "John"
