from django.urls import path

from .views.task import TaskCompleteViewSet, TaskCreateViewSet, TaskOperationViewSet

urlpatterns = [
    path("task/", TaskCreateViewSet.as_view({"post": "create"}), name="task-create"),
    path("task/<int:pk>/complete/", TaskCompleteViewSet.as_view({"post": "complete_task"}), name="task-complete"),
    path("tasks/", TaskOperationViewSet.as_view({"get": "list"}), name="task-list"),
    path(
        "task/<int:pk>/",
        TaskOperationViewSet.as_view(
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
