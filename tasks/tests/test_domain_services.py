import unittest
from datetime import datetime, timedelta
from tasks.domain.services import set_task_completion

class DummyTask:
    def __init__(self, completed=False, completed_at=None):
        self.completed = completed
        self.completed_at = completed_at

class TestSetTaskCompletion(unittest.TestCase):
    def test_sets_completed_at_when_completed(self):
        task = DummyTask(completed=False, completed_at=None)
        set_task_completion(task, True)
        self.assertIsNotNone(task.completed_at)
        self.assertIsInstance(task.completed_at, datetime)

    def test_clears_completed_at_when_not_completed(self):
        task = DummyTask(completed=True, completed_at=datetime.utcnow())
        set_task_completion(task, False)
        self.assertIsNone(task.completed_at)

    def test_does_not_overwrite_completed_at_if_already_set(self):
        now = datetime.utcnow() - timedelta(days=1)
        task = DummyTask(completed=True, completed_at=now)
        set_task_completion(task, True)
        self.assertEqual(task.completed_at, now)

if __name__ == '__main__':
    unittest.main() 