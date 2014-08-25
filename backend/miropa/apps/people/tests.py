# coding=utf-8
import json
from django.contrib.auth.models import User
from django.test import TestCase, Client


class RegisterUser(TestCase):
    def setUp(self):
        self._client = Client()

    def test_register_user_view(self):
        expected_data = {
            'id': 1,
            'username': 'john',
            'email': 'john@gmail.com',
            'is_active': True
        }
        response = self._client.post(
            path='/people/register/',
            data=json.dumps({
                'username': 'john', 'email': 'john@gmail.com', 'password1': '123', 'password2': '123'
            }),
            content_type='application/json'
        )
        expected_data = json.dumps(expected_data)
        response_data = json.loads(response.content)
        self.assertJSONEqual(expected_data, response_data)