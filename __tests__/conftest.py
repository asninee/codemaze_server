import pytest

from app.models import User


@pytest.fixture(scope="module")
def new_user():
    user = User(username="a", password="jkl")
    return user
