from django.urls import path

from .views import TasksGetView

urlpatterns = [
    path("tasks/", TasksGetView.as_view(), name="tasks-list"),
]
