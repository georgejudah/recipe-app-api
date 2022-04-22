from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create(**params)

#public api - no authentication
class PublicUserAPITests(TestCase):
    """Test the users API(Public)"""

    def Setup(self):
        self.client = APIClient()
    
    #https://www.django-rest-framework.org/api-guide/testing/#making-requests
    def test_create_valid_user_success(self):
        """Test Creating user with valid payload is successful"""
        payload = {
            'email': 'email@example.com',
            'password': 'testpass',
            'name': 'jxxtester'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exisits fails"""
        payload = {
            'email': 'email@example.com',
            'password': 'testpass',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'email@example.com',
            'password': 'test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()

        self.assertTrue(user_exists)

