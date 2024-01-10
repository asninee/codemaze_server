import pytest

from app.models import User, Rank


@pytest.fixture(scope="module")
def new_user():
    user = User(username="a", password="jkl")
    return user


@pytest.fixture(scope="module")
def new_rank():
    rank = Rank(name="Bronze", min_xp=0, max_xp=250)
    return rank
