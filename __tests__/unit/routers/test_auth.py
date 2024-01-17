from http import HTTPStatus


def test_valid_register(test_client):
    response = test_client.post(
        "/auth/register", json={"username": "testuser", "password": "jkl"}
    )
    assert response.status_code == HTTPStatus.CREATED


def test_invalid_register_one(test_client):
    response = test_client.post("/auth/register", json={"username": 0, "password": 1})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_invalid_register_two(test_client):
    response = test_client.post(
        "/auth/register", json={"username": "a", "password": "jkl"}
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_valid_login(test_client):
    response = test_client.post(
        "/auth/login", json={"username": "testuser", "password": "jkl"}
    )
    assert response.status_code == HTTPStatus.OK


def test_invalid_login_one(test_client):
    response = test_client.post("/auth/login", json={"username": 0, "password": 1})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_invalid_login_two(test_client):
    response = test_client.post(
        "/auth/login", json={"username": "z", "password": "jkl"}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_invalid_login_three(test_client):
    response = test_client.post(
        "/auth/login", json={"username": "a", "password": "jklm"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_valid_logout(test_client, log_in_user):
    access_token = log_in_user
    response = test_client.post(
        "/auth/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.OK
