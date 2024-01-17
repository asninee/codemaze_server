from flask import app
from app.models import User


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, password, avatar, xp, wins, losses and rank_id fields are defined correctly
    """
    assert new_user.username == "a"
    assert new_user.password_hash != "jkl"
    assert new_user.avatar == ""
    assert new_user.xp == 0
    assert new_user.wins == 0
    assert new_user.losses == 0
    assert new_user.rank_id == 1
    assert (
        new_user.__repr__() == f"User(username: {new_user.username}, xp: {new_user.xp})"
    )


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password("newpass")
    assert new_user.password_hash != "newpass"
    assert new_user.check_password("newpass")
    assert not new_user.check_password("newpass2")


def test_rank_up(new_user):
    """
    GIVEN an existing User
    WHEN the rank_up() function is called
    THEN check the related rank has been updated
    """
    new_user.rank_up()
    assert new_user.rank_id == 2
    assert new_user.rank_id != 1


def test_assign_random_avatar(new_user):
    """
    GIVEN an existing User
    WHEN the assign_random_avatar() function is called
    THEN check the avatar has been updated
    """
    new_user.assign_random_avatar()
    assert new_user.avatar != ""


# def test_find_by_username(new_user):
#     """
#     GIVEN an existing User
#     WHEN the find_by_username() function is called
#     THEN check that the related User object has been returned
#     """
#     fetched_user = User.find_by_username(new_user.username)
#     assert fetched_user == new_user
