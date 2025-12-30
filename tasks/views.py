from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from . import services


class TaskViewSet(viewsets.ViewSet):
    def list(self, request):
        status_filter = request.query_params.get("status")
        tasks = services.list_tasks(status_filter)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        task = services.get_task(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = services.create_task(**serializer.validated_data)
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        task = services.get_task(pk)
        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        task = services.update_task(task, **serializer.validated_data)
        return Response(TaskSerializer(task).data)

    def destroy(self, request, pk=None):
        task = services.get_task(pk)
        services.delete_task(task)
        return Response(status=status.HTTP_204_NO_CONTENT)
