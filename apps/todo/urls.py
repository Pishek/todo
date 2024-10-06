from django.urls import path

from .views.task import TaskViewSet

urlpatterns = [
    path("tasks/", TaskViewSet.as_view({"get": "list"}), name="task-list"),
    path("task/", TaskViewSet.as_view({"post": "create"}), name="task-create"),
    path(
        "task/<int:pk>/",
        TaskViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="task-detail",
    ),
]
