from http import HTTPStatus


def test_valid_create_session(test_client, log_in_user):
    access_token = log_in_user
    response = test_client.post(
        "/sessions",
        json={"problem_id": 1, "user_one_id": 3, "user_two_id": 8, "winner_id": 8},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.CREATED


def test_invalid_create_session_one(test_client, log_in_user):
    access_token = log_in_user
    response = test_client.post(
        "/sessions",
        json={
            "problem_id": 1,
            "user_one_id": 3,
            "user_two_id": 8,
            "winner_id": 9,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
