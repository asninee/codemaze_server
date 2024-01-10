def test_new_problem_with_fixture(new_problem):
    """
    GIVEN a Problem model
    WHEN a new Problem is created
    THEN check the title, content and rank_id fields are defined correctly
    """
    assert new_problem.title == "labore"
    assert (
        new_problem.content
        == "Commodo nostrud Lorem et deserunt commodo Lorem est officia reprehenderit sunt eiusmod Lorem ex amet. Mollit deserunt est amet aute cillum proident non ipsum deserunt nisi labore tempor irure non sunt. Sunt duis qui minim proident exercitation labore minim mollit aliquip fugiat anim. Est proident esse anim sint ut proident aute ullamco voluptate veniam dolore nulla. Do incididunt aliquip eu Lorem proident. Qui ad ullamco anim anim fugiat aliquip. Ut minim proident dolore."
    )
    assert new_problem.rank_id == 2
    assert (
        new_problem.__repr__()
        == f"Problem(title: {new_problem.title}, rank_id: {new_problem.rank_id})"
    )
