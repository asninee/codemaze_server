from app.models import User


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name and password fields are defined correctly
    """
    assert new_user.username == "a"
    assert new_user.password_hash != "jkl"
    assert new_user.xp == 0
    assert new_user.wins == 0
    assert new_user.losses == 0
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
