import pytest

from be_task_ca.user.model import User
from be_task_ca.user.repository import UserRepoInMemory
from be_task_ca.user.schema import UserPrivate


@pytest.fixture()
def first_user():
    return User(
        first_name="First",
        last_name="User",
        email="user1@example.com",
        hashed_password="password",
        shipping_address="123 Main St",
        cart_items=[],
    )


@pytest.fixture()
def second_user():
    return User(
        first_name="Second",
        last_name="User",
        email="user2@example.com",
        hashed_password="password",
        shipping_address="123 Main St",
        cart_items=[],
    )


@pytest.fixture(scope="function")
def user_store(first_user, second_user):
    return {first_user.id: first_user, second_user.id: second_user}


@pytest.fixture(scope="function")
def user_repo(user_store):
    return UserRepoInMemory(users=user_store, cart_items={})


def test_save_user(user_repo, user_store):
    user_private = UserPrivate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password",
        shipping_address="123 Main St",
    )

    assert len(user_store) == 2

    user_schema = user_repo.save_user(user_private)

    assert user_schema.email == "john.doe@example.com"
    assert user_schema.first_name == "John"
    assert user_schema.last_name == "Doe"

    assert len(user_store) == 3
    assert user_schema.id in user_store


def test_find_user_by_email(user_repo, second_user):
    email = second_user.email

    user_schema = user_repo.find_user_by_email(email)

    assert user_schema is not None
    assert user_schema.id == second_user.id
    assert user_schema.email == email
    assert user_schema.first_name == second_user.first_name


def test_find_user_by_id(user_repo, second_user):
    user_schema = user_repo.find_user_by_id(second_user.id)

    assert user_schema is not None
    assert user_schema.id == second_user.id
    assert user_schema.first_name == second_user.first_name
