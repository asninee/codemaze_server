def test_new_session_with_fixture(new_session):
    """
    GIVEN a Session model
    WHEN a new Session is created
    THEN check the problem_id field is defined correctly
    """
    assert new_session.problem_id == 1
    assert new_session.__repr__() == f"Session(problem_id: {new_session.problem_id})"
