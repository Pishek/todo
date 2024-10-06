import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from tests.utils import fake


@pytest.fixture()
def user_password() -> str:
    return fake.person.password()


@pytest.fixture()
def user(user_password: str) -> User:
    return User.objects.create_user(username=fake.person.name(), password=user_password, email=fake.person.password())


@pytest.fixture()
def user_token(user: User) -> Token:
    token, created = Token.objects.get_or_create(user=user)
    return token
