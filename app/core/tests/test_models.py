from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(email='test@hjoeftung.org', password='hackme'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""

        email = 'test@hjoeftung.org'
        password = 'hackme'
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
        email = 'test@hjoeftung.org'
        user = get_user_model().objects.create_superuser(
            email=email,
            password='somepass'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self. assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Steak and mushroom sauce",
            time=5,
            price=100.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        new_uuid = 'test-uuid'
        mock_uuid.return_value = new_uuid
        file_path = models.recipe_image_file_path(None, 'image.jpg')

        exp_path = f'uploads/recipe/{new_uuid}.jpg'
        self.assertEqual(str(file_path), exp_path)
