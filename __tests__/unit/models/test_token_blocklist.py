def test_new_token_blocklist_entry_with_fixture(new_token_blocklist_entry):
    """
    GIVEN a TokenBlocklist model
    WHEN a new TokenBlocklist entry is created
    THEN check the jti field is defined correctly
    """
    assert new_token_blocklist_entry.jti == "MZAIfabl9X"
    assert (
        new_token_blocklist_entry.__repr__()
        == f"TokenBlocklist(jti: {new_token_blocklist_entry.jti})"
    )
