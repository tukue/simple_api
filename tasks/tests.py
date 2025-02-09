from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
from .models import Task

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('tasks-api')

    def test_get_api_endpoint(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

    def test_post_api_endpoint(self):
        data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'completed': False
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_data(self):
        data = {}
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_api_endpoint(self):
        # First, create the resource
        task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            completed=False
        )
        updated_data = {
            'title': 'Updated Task',
            'description': 'This is an updated test task',
            'completed': True
        }
        response = self.client.put(
            reverse('task-detail-api', args=[task.id]),
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_api_endpoint(self):
        # First, create the resource
        task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            completed=False
        )
        response = self.client.delete(reverse('task-detail-api', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)