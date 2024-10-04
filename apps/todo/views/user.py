from typing import Any

from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class CustomUserViewSet(UserViewSet):
    """Регистрация пользователя"""

    @extend_schema(methods=["post"], tags=["User auth"])
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)


class CustomTokenCreateView(TokenCreateView):
    """Логин, создание токена"""

    @extend_schema(methods=["post"], tags=["User auth"])
    def post(self, request: Request, **kwargs: Any) -> Response:
        return super().post(request, **kwargs)


class CustomTokenDestroyView(TokenDestroyView):
    """Логаут, удаление токена"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(methods=["post"], tags=["User auth"])
    def post(self, request: Request) -> Response:
        return super().post(request)
