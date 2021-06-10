from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""

        email = "test@hjoeftung.org"
        password = "hackme"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that email for a new user normalized"""
        email = "test@HJOEFTUNG.ORG"
        user = get_user_model().objects.create_user(
            email=email,
            password="123"
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None)

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = "test@hjoeftung.org"
        user = get_user_model().objects.create_superuser(
            email=email,
            password="somepass"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
