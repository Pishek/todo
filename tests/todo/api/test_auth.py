from unittest.mock import ANY

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.utils import fake


@pytest.mark.django_db
def test_registration_ok(api_client: APIClient) -> None:
    payload = {"username": fake.person.name(), "password": fake.person.password(), "email": fake.person.email()}

    response = api_client.post("/auth/register/", data=payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {"username": payload["username"], "email": payload["email"], "id": ANY}


@pytest.mark.django_db
def test_login_ok(api_client: APIClient, user: User, user_password: str) -> None:
    payload = {"username": user.username, "password": user_password}
    response = api_client.post("/auth/login/", data=payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"auth_token": ANY}


@pytest.mark.django_db
def test_logout_ok(api_client: APIClient, user_token: Token) -> None:
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token.key)
    response = api_client.post("/auth/logout/", format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
