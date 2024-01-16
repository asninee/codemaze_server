def test_new_example_with_fixture(new_example):
    """
    GIVEN a Example model
    WHEN a new Example is created
    THEN check the input, output and explanation
    """
    assert new_example.input == "cillum"
    assert new_example.output == "adipisicing occaecat"
    assert (
        new_example.explanation
        == "Commodo exercitation in nulla aliqua reprehenderit magna reprehenderit adipisicing. Do pariatur consequat eu ad ut eu tempor elit. Eiusmod esse Lorem aliquip pariatur ea. Fugiat consectetur do est et magna labore sunt tempor quis."
    )
    assert new_example.test_case == "occaecat do irure dolor"
    assert new_example.__repr__() == f"Example(problem_id: {new_example.problem_id})"
