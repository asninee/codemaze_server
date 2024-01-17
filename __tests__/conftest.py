import pytest
from app import create_app
from app.extensions import db

from app.models import Example, Session, TokenBlocklist, User, Rank, Problem


@pytest.fixture(scope="module")
def test_client():
    app = create_app()

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

            User.query.filter(User.username == "testuser").delete()
            db.session.commit()


@pytest.fixture(scope="function")
def log_in_user(test_client):
    response = test_client.post("auth/login", json={"username": "a", "password": "jkl"})

    yield response.json["access_token"]

    test_client.get("auth/logout")


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
        description="Commodo nostrud Lorem et deserunt commodo Lorem est officia reprehenderit sunt eiusmod Lorem ex amet. Mollit deserunt est amet aute cillum proident non ipsum deserunt nisi labore tempor irure non sunt. Sunt duis qui minim proident exercitation labore minim mollit aliquip fugiat anim. Est proident esse anim sint ut proident aute ullamco voluptate veniam dolore nulla. Do incididunt aliquip eu Lorem proident. Qui ad ullamco anim anim fugiat aliquip. Ut minim proident dolore.",
        rank_id=2,
    )
    return problem


@pytest.fixture(scope="module")
def new_example():
    example = Example(
        problem_id=1,
        input="cillum",
        output="adipisicing occaecat",
        explanation="Commodo exercitation in nulla aliqua reprehenderit magna reprehenderit adipisicing. Do pariatur consequat eu ad ut eu tempor elit. Eiusmod esse Lorem aliquip pariatur ea. Fugiat consectetur do est et magna labore sunt tempor quis.",
        test_case="occaecat do irure dolor",
    )
    return example


@pytest.fixture(scope="module")
def new_session():
    session = Session(problem_id=1, winner_id=3)
    return session


@pytest.fixture(scope="module")
def new_token_blocklist_entry():
    blocklist_entry = TokenBlocklist(jti="MZAIfabl9X")
    return blocklist_entry
