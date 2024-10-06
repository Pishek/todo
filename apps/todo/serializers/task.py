from rest_framework import serializers

from apps.todo.models import TaskOrm


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOrm
        fields = ["id", "title"]


class TaskListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOrm
        fields = ["id", "title", "description", "status", "priority", "due_date", "created_at", "completed_at"]
