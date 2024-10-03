from typing import Any

from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class TasksGetView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        data = [{"id": 1}, {"id": 2}]
        return Response(data)
