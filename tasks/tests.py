from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Task
from django.conf import settings

class TaskAPIViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task_url = reverse('tasks-api')  # Replace with your actual URL name
        self.task_detail_url = lambda pk: reverse('task-detail-api', args=[pk])  # Replace with your actual URL name
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'completed': False
        }
        self.task = Task.objects.create(**self.task_data)

    def test_get_tasks(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # Check if paginated response contains 'results'

    def test_post_task(self):
        new_task_data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'completed': False
        }
        response = self.client.post(
            self.task_url,
            data=new_task_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], new_task_data['title'])

    def test_put_task(self):
        updated_data = {
            'title': 'Updated Task',
            'description': 'This is an updated task',
            'completed': True
        }
        response = self.client.put(
            self.task_detail_url(self.task.id),
            data=updated_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_delete_task(self):
        response = self.client.delete(self.task_detail_url(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_pagination(self):
        """Test that task pagination works."""
        for i in range(15):  # Create 15 tasks
            Task.objects.create(title=f"Task {i}", description="Paginated task", completed=False)
        response = self.client.get(self.task_url + '?page=2')  # Request the second page
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertTrue(len(response.data['results']) <= 10)  # Page size is 10 

    
    def test_get_task_detail(self):
        """Test retrieving a single task by ID."""
        response = self.client.get(self.task_detail_url(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title) 
    
    