from flask import json
import requests, responses
from http import HTTPStatus


def test_valid_random_problem(test_client, log_in_user):
    access_token = log_in_user
    response = test_client.get(
        "/problems/random", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.OK


def test_valid_generate_problem(test_client, log_in_user):
    access_token = log_in_user
    mock_problem = json.dumps(
        {
            "title": "labore",
            "description": "Commodo nostrud Lorem et deserunt commodo Lorem est officia reprehenderit sunt eiusmod Lorem ex amet. Mollit deserunt est amet aute cillum proident non ipsum deserunt nisi labore tempor irure non sunt. Sunt duis qui minim proident exercitation labore minim mollit aliquip fugiat anim. Est proident esse anim sint ut proident aute ullamco voluptate veniam dolore nulla. Do incididunt aliquip eu Lorem proident. Qui ad ullamco anim anim fugiat aliquip. Ut minim proident dolore.",
            "rank_id": 2,
        }
    )
    responses.add(
        responses.POST,
        "http://localhost:3000/problems/generate",
        headers={"Authorization": f"Bearer {access_token}"},
        json=mock_problem,
        status=HTTPStatus.CREATED,
    )

    response = test_client.post(
        "/problems/generate", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.CREATED
