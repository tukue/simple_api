from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Use the correct URL pattern name from your urls.py
        self.url = reverse('tasks-api')  # or whatever name you've defined in urls.py

    def test_get_api_endpoint(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

    def test_post_api_endpoint(self):
        data = {
            'key': 'value'
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
        data = {
            'key': 'updated_value'
        }
        response = self.client.put(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_api_endpoint(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
