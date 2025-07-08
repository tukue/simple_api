from datetime import datetime
from django.utils import timezone

def set_task_completion(task, completed: bool):
    """
    Set the completed_at field based on the completed status.
    Args:
        task: The task instance (should have 'completed' and 'completed_at' attributes).
        completed (bool): Whether the task is completed.
    """
    if completed and not task.completed_at:
        task.completed_at = timezone.now()
    elif not completed:
        task.completed_at = None
    return task 