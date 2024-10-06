from unittest.mock import ANY

import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.todo.models import PriorityEnum, StatusEnum, TaskOrm
from tests.utils import fake


@pytest.mark.django_db
def test_create_task_ok(api_client: APIClient, user_token: Token) -> None:
    payload = {
        "title": fake.text.word(),
        "description": fake.text.text(),
        "status": StatusEnum.PENDING,
        "priority": PriorityEnum.LOW,
    }
    expected_data = {"id": ANY, "title": payload["title"]}

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token.key)
    response = api_client.post("/todo/task/", data=payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data


@pytest.mark.django_db
def test_retrieve_task_ok(api_client: APIClient, user_token: Token, user_tasks: list[TaskOrm]) -> None:
    expected_data = {
        "id": user_tasks[0].pk,
        "title": user_tasks[0].title,
        "description": user_tasks[0].description,
        "status": user_tasks[0].status,
        "priority": user_tasks[0].priority,
        "due_date": user_tasks[0].due_date,
        "created_at": ANY,
        "completed_at": user_tasks[0].completed_at,
    }

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token.key)
    response = api_client.get(f"/todo/task/{user_tasks[0].pk}/", format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_get_list_tasks_ok(api_client: APIClient, user_token: Token, user_tasks: list[TaskOrm]) -> None:
    expected_data = [
        {
            "id": x.pk,
            "title": x.title,
            "description": x.description,
            "status": x.status,
            "priority": x.priority,
            "due_date": x.due_date,
            "created_at": ANY,
            "completed_at": x.completed_at,
        }
        for x in user_tasks
    ]

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token.key)
    response = api_client.get("/todo/tasks/", format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"] == expected_data


@pytest.mark.django_db
def test_patch_task_ok(api_client: APIClient, user_token: Token, user_tasks: list[TaskOrm]) -> None:
    payload = {"title": "SuperHeroBatmen123"}
    expected_data = {
        "id": user_tasks[0].pk,
        "description": user_tasks[0].description,
        "status": user_tasks[0].status,
        "priority": user_tasks[0].priority,
        "due_date": user_tasks[0].due_date,
        "created_at": ANY,
        "completed_at": user_tasks[0].completed_at,
        "title": payload["title"],
    }

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token.key)
    response = api_client.patch(f"/todo/task/{user_tasks[0].pk}/", data=payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_put_task_ok(api_client: APIClient, user_token: Token, user_tasks: list[TaskOrm]) -> None:
    payload = {"title": "SuperHeroBatmen123", "priority": PriorityEnum.HIGH}
    expected_data = {
        "id": user_tasks[0].pk,
        "description": user_tasks[0].description,
        "status": user_tasks[0].status,
        "due_date": user_tasks[0].due_date,
        "created_at": ANY,
        "completed_at": user_tasks[0].completed_at,
        "title": payload["title"],
        "priority": payload["priority"],
    }

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token.key)
    response = api_client.patch(f"/todo/task/{user_tasks[0].pk}/", data=payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_delete_task_ok(api_client: APIClient, user_token: Token, user_tasks: list[TaskOrm]) -> None:

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token.key)
    response = api_client.delete(f"/todo/task/{user_tasks[0].pk}/", format="json")

    task_1 = TaskOrm.objects.filter(pk=user_tasks[0].pk).first()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert task_1 is None
