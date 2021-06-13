from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipes.serializers import TagSerializer


TAGS_URL = reverse('recipes:tag-list')


def create_tag(user, name='dessert'):
    return Tag.objects.create(user=user, name=name)


def create_user(email='test@hjoeftung.org', password='hackme', name='Vasyan'):
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name
    )


class TagsAPIPublicTests(TestCase):
    """Test the public tags API"""

    def test_get_tags_list_unauthorized(self):
        """Test that unauthorized user cannot get tags list"""
        self.client = APIClient()
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAPIPrivateTests(TestCase):
    """Test the private tags API"""

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_tags_list(self):
        create_tag(user=self.user, name='vegan')
        create_tag(user=self.user, name='dessert')
        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_users_tags(self):
        """Test getting tags that belong to authenticated user"""
        user2 = create_user(email='test1@hjoeftung.org')
        create_tag(user=user2, name='fruity')
        tag = create_tag(user=self.user, name='comfort food')
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test that the tag is successfully created"""
        payload = {'name': 'fixing'}
        response = self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test that tag cannot be created with an invalid name"""
        payload = {'name': ''}
        response = self.client.post(TAGS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
