from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import serializers



class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class TasksGetView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        data = [{'id': 1}, {'id': 2}]
        return Response(data)