import json

import pytest


@pytest.fixture
def create_user(client):
    def do_create_user(**kwargs):
        data = {
            "name": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        data.update(kwargs)
        return client.post(
            "/user/create/",
            data=json.dumps(data),
            content_type="application/json",
        )

    return do_create_user


@pytest.mark.django_db
class TestCreateUserAPI:
    def test_create_user(self, client):
        response = client.post(
            "/user/create/",
            data=json.dumps(
                {
                    "name": "testuser",
                    "email": "testuser@example.com",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 201
        assert response.json()["name"] == "testuser"
        assert "id" in response.json()
        print(response.json())

    def test_create_user_duplicate_email(self, client, create_user):
        create_user()
        response = create_user()
        assert response.status_code == 400
        assert response.json()["email"] == ["user with this email already exists."]

    def test_password_strength(self, client):
        response = client.post(
            "/user/create/",
            data=json.dumps(
                {
                    "name": "testuser",
                    "email": "testuser@example.com",
                    "password": "weak",  # < 8 chars
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert response.json()["password"] == [
            "Ensure this field has at least 8 characters."
        ]


@pytest.mark.django_db
class TestUserLoginAPI:
    def test_create_token(self, client, create_user):
        create_user()
        response = client.post(
            "/user/token/",
            data=json.dumps(
                {
                    "email": "testuser@example.com",
                    "password": "testpassword",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert "token" in response.json()
