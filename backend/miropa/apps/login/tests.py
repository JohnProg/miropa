# coding: utf-8
"""
Test for Login.
"""
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client


class LoginTest(TestCase):
    def setUp(self):
        self._client = Client()
        User.objects.create_user(
            id=1,
            username='pepito@cursostotales.com',
            email='pepito@cursostotales.com',
            password='123456'
        )

    def test_login_view(self):
        """ Tests login view """
        expected_data = {
            'id': 1,
            'username': 'pepito@cursostotales.com',
            'is_active': True
        }

        response = self._client.post(
            path='/login/',
            data=json.dumps(
                {'username': 'pepito@cursostotales.com', 'password': '123456'}),
            content_type='application/json'
        )

        expected_data = json.dumps(expected_data)
        response_data = json.loads(response.content)

        self.assertJSONEqual(expected_data, response_data)

    def test_logout_view(self):
        """ Tests logout view"""
        expected_data = {
            'success': True
        }
        response = self._client.post(
            path='/logout/'
        )
        expected_data = json.dumps(expected_data)
        response_data = json.loads(response.content)
        self.assertJSONEqual(expected_data, response_data)