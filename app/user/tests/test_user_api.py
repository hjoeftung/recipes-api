from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the public users API"""
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successuful"""
        payload = {
            'email': 'test@hjoeftung.org',
            'password': 'superpass',
            'name': 'Vasya'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.filter(email=payload['email'])
        self.assertTrue(user[0].check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_create_user_exists(self):
        payload = {
            'email': 'test@hjoeftung.org',
            'password': 'superpass',
            'name': 'Vasya'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the pass is more than 5 characters"""
        payload = {
            'email': 'test@hjoeftung.org',
            'password': 'pass',
            'name': 'Vasya'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_successful(self):
        """Test that the token is created for the user"""
        payload = {
            'email': 'test@hjoeftung.org',
            'password': 'pass',
            'name': 'Vasya'
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created with invalid credentials"""
        create_user(**{
            'email': 'test@hjoeftung.org',
            'password': 'superpass',
            'name': 'Vasya'
        })

        payload = {
            'email': 'test@hjoeftung.org',
            'password': 'psssst',
            'name': 'Vasya'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""
        payload = {
            'email': 'test@hjoeftung.org',
            'password': 'psssst',
            'name': 'Vasya'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        payload = {
            'email': 'test@hjoeftung.org',
            'name': 'Vasya'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test the private user API"""

    def setUp(self):
        self.user = create_user(**{
            'email': 'test@hjoeftung.org',
            'password': 'superpass',
            'name': 'Vasya'
        })
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def post_me_not_allowed(self):
        """Test that post is not allowed on me/ url"""
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for an authenticated user"""
        payload = {'password': 'hackthem', 'user': 'vasyan@padik.ru'}
        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
