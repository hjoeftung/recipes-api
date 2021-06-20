from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipes.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITests(TestCase):
    """Test public ingredients API"""

    def test_get_ingredients_unauthorized(self):
        self.user = get_user_model().objects.create_user(
            email='test@hjoeftung.org',
            password='hackme',
            name='Vasyan'
        )
        self.client = APIClient()
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test private ingredients API"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email='test@hjoeftung.org',
            password='hackme',
            name='Vasyan'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_ingredients_authorized(self):
        """Test getting ingredients list by authorized user"""
        Ingredient.objects.create(user=self.user, name='tomato')
        Ingredient.objects.create(user=self.user, name='cucumber')
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_ingredients_limited_to_user(self):
        """Test that ingredients list is specific to the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='admin@hjoeftung.org',
            password='nopass',
            name='Stasyan'
        )
        Ingredient.objects.create(user=user2, name='tomato')
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='cucumber'
        )
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test that ingredient is successfully created"""
        payload = {'name': 'cucumber'}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ingredient_invalid(self):
        """Test that ingredient with invalid name is not created"""
        payload = {'name': ''}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
