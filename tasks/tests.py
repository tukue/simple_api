from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from tasks.infrastructure.models import Task

class TaskAPIViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task_url = reverse('tasks-api')
        self.task_detail_url = lambda pk: reverse('task-detail-api', args=[pk])
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'completed': False
        }
        self.task = Task.objects.create(**self.task_data)

    def test_list_tasks_returns_paginated_results(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_create_task_with_valid_data(self):
        new_task_data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'completed': False
        }
        response = self.client.post(self.task_url, data=new_task_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], new_task_data['title'])

    def test_create_task_with_invalid_data(self):
        invalid_data = {'title': '', 'description': '', 'completed': False}
        response = self.client.post(self.task_url, data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_retrieve_existing_task(self):
        response = self.client.get(self.task_detail_url(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_retrieve_nonexistent_task_returns_404(self):
        response = self.client.get(self.task_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_with_valid_data(self):
        updated_data = {
            'title': 'Updated Task',
            'description': 'This is an updated task',
            'completed': True
        }
        response = self.client.put(self.task_detail_url(self.task.id), data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_update_task_with_invalid_data(self):
        invalid_data = {'title': '', 'description': '', 'completed': False}
        response = self.client.put(self.task_detail_url(self.task.id), data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_update_nonexistent_task_returns_404(self):
        updated_data = {'title': 'Updated', 'description': 'Updated', 'completed': True}
        response = self.client.put(self.task_detail_url(9999), data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_task(self):
        response = self.client.delete(self.task_detail_url(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_nonexistent_task_returns_404(self):
        response = self.client.delete(self.task_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_pagination_multiple_pages(self):
        for i in range(15):
            Task.objects.create(title=f"Task {i}", description="Paginated task", completed=False)
        response = self.client.get(self.task_url + '?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertTrue(len(response.data['results']) <= 10) 
