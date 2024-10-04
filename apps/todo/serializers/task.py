from rest_framework import serializers

from apps.todo.models import TaskOrm


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOrm
        fields = ["id", "title", "description", "status", "priority", "due_date", "completed_at"]
