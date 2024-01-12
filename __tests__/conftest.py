import pytest

from app.models import Session, TokenBlocklist, User, Rank, Problem


@pytest.fixture(scope="module")
def new_user():
    user = User(username="a", password="jkl")
    return user


@pytest.fixture(scope="module")
def new_rank():
    rank = Rank(name="Bronze", min_xp=0, max_xp=250)
    return rank


@pytest.fixture(scope="module")
def new_problem():
    problem = Problem(
        title="labore",
        content="Commodo nostrud Lorem et deserunt commodo Lorem est officia reprehenderit sunt eiusmod Lorem ex amet. Mollit deserunt est amet aute cillum proident non ipsum deserunt nisi labore tempor irure non sunt. Sunt duis qui minim proident exercitation labore minim mollit aliquip fugiat anim. Est proident esse anim sint ut proident aute ullamco voluptate veniam dolore nulla. Do incididunt aliquip eu Lorem proident. Qui ad ullamco anim anim fugiat aliquip. Ut minim proident dolore.",
        rank_id=2,
    )
    return problem


@pytest.fixture(scope="module")
def new_session():
    session = Session(problem_id=1, winner_id=3)
    return session


@pytest.fixture(scope="module")
def new_token_blocklist_entry():
    blocklist_entry = TokenBlocklist(jti="MZAIfabl9X")
    return blocklist_entry
