from app.models import Rank


def test_new_rank_with_fixture(new_rank):
    """
    GIVEN a Rank model
    WHEN a new Rank is created
    THEN check the name, min_xp and max_xp fields are defined correctly
    """
    assert new_rank.name == "Bronze"
    assert new_rank.min_xp == 0
    assert new_rank.max_xp == 250
    assert (
        new_rank.__repr__()
        == f"Rank(name: {new_rank.name}, min_xp: {new_rank.min_xp}, max_xp: {new_rank.max_xp})"
    )
