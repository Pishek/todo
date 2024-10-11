from rest_framework import serializers

from apps.todo.models import TaskOrm


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOrm
        fields = ["id", "title", "description", "priority"]


class TaskListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskOrm
        fields = ["id", "title", "description", "status", "priority", "duration_in_days", "created_at", "completed_at"]


class TaskCompleteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    duration_in_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskOrm
        fields = ["id", "status", "created_at", "completed_at", "duration_in_days"]
