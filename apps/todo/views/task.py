from typing import Any

from django.db.models import QuerySet
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.todo.exceptions import UserTasksNotFoundException
from apps.todo.models import TaskOrm
from apps.todo.serializers.task import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskOrm.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        user_id = self.request.user.id
        queryset = self.queryset.filter(user_id=user_id)
        if not queryset.exists():
            raise UserTasksNotFoundException
        return queryset

    def get_object(self) -> TaskOrm:
        try:
            return super().get_object()
        except Http404:
            raise UserTasksNotFoundException

    def perform_create(self, serializer: Serializer) -> None:
        user_id = self.request.user.id
        serializer.save(user_id=user_id)

    @extend_schema(methods=["get"], tags=["Tasks"])
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(methods=["get"], tags=["Tasks"])
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(methods=["post"], tags=["Tasks"])
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(methods=["put"], tags=["Tasks"])
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(methods=["patch"], tags=["Tasks"])
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(methods=["delete"], tags=["Tasks"])
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)
