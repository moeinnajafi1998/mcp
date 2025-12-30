from django.shortcuts import get_object_or_404
from .models import Task


def list_tasks(status: str | None = None):
    qs = Task.objects.all().order_by("-created_at")
    if status:
        qs = qs.filter(status=status)
    return qs


def get_task(task_id: int) -> Task:
    return get_object_or_404(Task, id=task_id)


def create_task(**data) -> Task:
    return Task.objects.create(**data)


def update_task(task: Task, **data) -> Task:
    for field, value in data.items():
        setattr(task, field, value)
    task.save()
    return task


def delete_task(task: Task) -> None:
    task.delete()
