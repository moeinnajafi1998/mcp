from django.forms.models import model_to_dict
from tasks.models import Task


def task_to_dict(task: Task):
    """Convert Task model to dict with ISO datetime strings"""
    data = model_to_dict(task)
    data["created_at"] = task.created_at.isoformat()
    data["updated_at"] = task.updated_at.isoformat()
    return data


def list_tasks(status: str | None = None):
    qs = Task.objects.all().order_by("-created_at")
    if status:
        if status not in Task.Status.values:
            raise ValueError("Invalid status")
        qs = qs.filter(status=status)
    return [task_to_dict(task) for task in qs]


def get_task_by_id(id: int):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        raise ValueError("Task not found")
    return task_to_dict(task)


def create_task(title: str, description: str = "", status: str = Task.Status.PENDING):
    if status not in Task.Status.values:
        raise ValueError("Invalid status")
    task = Task.objects.create(title=title, description=description, status=status)
    return task_to_dict(task)


def update_task_status(id: int, status: str):
    if status not in Task.Status.values:
        raise ValueError("Invalid status")
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        raise ValueError("Task not found")
    task.status = status
    task.save()
    return task_to_dict(task)


def delete_task(id: int):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        raise ValueError("Task not found")
    task.delete()
    return {"message": "Task deleted"}


TOOL_REGISTRY = {
    "list_tasks": list_tasks,
    "get_task_by_id": get_task_by_id,
    "create_task": create_task,
    "update_task_status": update_task_status,
    "delete_task": delete_task,
}
